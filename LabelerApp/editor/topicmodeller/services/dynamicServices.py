# -*- coding: utf-8 -*-
import json
import os

from editor.topicmodeller.utils.consts import linkListPath
from editor.webcrawler.webcrawler.scripts.dynamic_linklist_parse import parse_dynamic_linklist

__author__ = 'forestg'

# logging bekapcsolása:
import logging

def linkListHandling(text):
    print("text arrived, saving:", text)

    textSplit = text.split()

    # formattedLinks = ["http://" + s for s in textSplit if "http://" not in s]
    # formattedLinks.append(s for s in textSplit if "http://" in s)
    formattedLinks = []
    for s in textSplit:
        if "http://" in s:
            formattedLinks.append(s)
        else:
            formattedLinks.append("http://"+s)

    print(formattedLinks)

    if (os.path.isfile(linkListPath)):
        os.remove(linkListPath)
    with open(linkListPath, 'w') as f:
        json.dump(formattedLinks, f)

def parseWebsitesFromLinkList():
    parse_dynamic_linklist()




