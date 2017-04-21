# -*- coding: utf-8 -*-
import csv
from collections import defaultdict

__author__ = 'forestg'


def countTopicsInGivenCsv():
    path = "/home/forestg/projects/dipterv/dump.csv"
    # path = "/home/forestg/projects/dipterv/dump_smaller.csv"
    frequencies_dict = defaultdict(int)
    with open(path, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar=' ')
        for row in csvreader:
            for word in row[1].split():
                frequencies_dict[word] += 1

    # kitöröljük a hibákat
    for key in frequencies_dict.keys():
        if(frequencies_dict[key] < 2):
            del frequencies_dict[key]

    print ("categories:", len(frequencies_dict))
    print (frequencies_dict)

countTopicsInGivenCsv()
