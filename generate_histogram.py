"""Reads a har file from the filesystem, converts to CSV, then dumps to
stdout.
"""
import argparse
import json
import csv
from urllib.parse import urlparse
from tld import get_tld
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def main(harfile_path):
    """Reads a har file from the filesystem, converts to CSV, then dumps to
    stdout.
    """
    first_party = harfile_path.split(".")[0]+".com"
    query_count = 0
    third_party=[]
    tp_count = 0
    data_sum = 0
    harfile = open(harfile_path, encoding="utf8")
    harfile_json = json.loads(harfile.read())
    i = 0
    

    with open(harfile_path[:-4] + '.csv', 'w') as f:
        #csv_file = csv.writer(f)
        #csv_file.writerow(['id', 'url', 'hostname', 'size (bytes)',
        #    'size (kilobytes)', 'mimetype'])

        for entry in harfile_json['log']['entries']:
            i = i + 1
            url = entry['request']['url']
            urlparts = urlparse(entry['request']['url'])
            size_bytes = entry['response']['bodySize']
            size_kilobytes = float(entry['response']['bodySize'])/1024
            mimetype = 'unknown'
            if 'mimeType' in entry['response']['content']:
                mimetype = entry['response']['content']['mimeType']
           # csv_file.writerow([i, url, urlparts.hostname, size_bytes,
           #     size_kilobytes, mimetype])
            query_count += 1
            res = get_tld(url, as_object=True)
            if res.fld != first_party:
            	third_party.append(res.fld)
            data_sum += abs(size_kilobytes)
    tp_count = len(list(set(third_party)))
    return(query_count, tp_count, data_sum)


if __name__ == '__main__':
    sites = ["macys.har", "cnn.har", "bankofamerica.har","macys_adp.har", "cnn_adp.har", "bankofamerica_adp.har","macys_ghost.har", "cnn_ghost.har", "bankofamerica_ghost.har","macys_pb.har", "cnn_pb.har", "bankofamerica_pb.har"]
    query_distribution = []
    tp_distribution = []
    data_sum_distribution = []
    for index, site in enumerate(sites):
    	query_count, tp_count, data_sum = main(site)
    	query_distribution.append(query_count)
    	tp_distribution.append(tp_count)
    	data_sum_distribution.append(data_sum)

    distribution1 = query_distribution[:3]
    distribution2 = query_distribution[3:6]
    distribution3 = query_distribution[6:9]
    distribution4 = query_distribution[9:]
    barWidth=0.15
    r1 = np.arange(len(distribution1))
    r2 = [x + barWidth*1.15 for x in r1]
    r3 = [x + barWidth*1.15 for x in r2]
    r4 = [x + barWidth*1.15 for x in r3]
    plt.bar(r1, distribution1, color='red', width=barWidth, edgecolor='black', label='No Extension')
    plt.bar(r2, distribution2, color='blue', width=barWidth, edgecolor='black', label='Adblock Plus')
    plt.bar(r3, distribution3, color='green', width=barWidth, edgecolor='black', label='Ghostery')
    plt.bar(r4, distribution4, color='lime', width=barWidth, edgecolor='black', label='Privacy Badger')
    plt.xlabel("Site")
    plt.title('Total queries')
    plt.xticks([r + barWidth for r in range(len(distribution1))], ["macys", "cnn", "bankofamerica"])
    plt.ylabel('Count of queries')
    plt.legend()
    plt.show()

    distribution1 = tp_distribution[:3]
    distribution2 = tp_distribution[3:6]
    distribution3 = tp_distribution[6:9]
    distribution4 = tp_distribution[9:]
    barWidth=0.15
    r1 = np.arange(len(distribution1))
    r2 = [x + barWidth*1.15 for x in r1]
    r3 = [x + barWidth*1.15 for x in r2]
    r4 = [x + barWidth*1.15 for x in r3]
    plt.bar(r1, distribution1, color='red', width=barWidth, edgecolor='black', label='No Extension')
    plt.bar(r2, distribution2, color='blue', width=barWidth, edgecolor='black', label='Adblock Plus')
    plt.bar(r3, distribution3, color='green', width=barWidth, edgecolor='black', label='Ghostery')
    plt.bar(r4, distribution4, color='lime', width=barWidth, edgecolor='black', label='Privacy Badger')
    plt.xlabel("Site")
    plt.title('Third party queries')
    plt.xticks([r + barWidth for r in range(len(distribution1))], ["macys", "cnn", "bankofamerica"])
    plt.ylabel('Count of queries')
    plt.legend()
    plt.show()

    distribution1 = data_sum_distribution[:3]
    distribution2 = data_sum_distribution[3:6]
    distribution3 = data_sum_distribution[6:9]
    distribution4 = data_sum_distribution[9:]
    barWidth=0.15
    r1 = np.arange(len(distribution1))
    r2 = [x + barWidth*1.15 for x in r1]
    r3 = [x + barWidth*1.15 for x in r2]
    r4 = [x + barWidth*1.15 for x in r3]
    plt.bar(r1, distribution1, color='red', width=barWidth, edgecolor='black', label='No Extension')
    plt.bar(r2, distribution2, color='blue', width=barWidth, edgecolor='black', label='Adblock Plus')
    plt.bar(r3, distribution3, color='green', width=barWidth, edgecolor='black', label='Ghostery')
    plt.bar(r4, distribution4, color='lime', width=barWidth, edgecolor='black', label='Privacy Badger')
    plt.xlabel("Site")
    plt.title('Downloaded content')
    plt.xticks([r + barWidth for r in range(len(distribution1))], ["macys", "cnn", "bankofamerica"])
    plt.ylabel('kilobytes')
    plt.legend()
    plt.show()
