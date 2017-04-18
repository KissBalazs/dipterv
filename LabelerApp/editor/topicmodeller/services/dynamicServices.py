# -*- coding: utf-8 -*-
import json
import os

from editor.topicmodeller.utils.consts import linkListPath, linkListDocumentsPath, DynamicTopicsPath
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

def topicModelDynamic():
    #1. megnyitjuk a dokumentumteret.
    path = linkListDocumentsPath
    if (os.path.exists(path)):
        with open(path) as data_file:
            document_array = json.load(data_file)
    else:
        raise ValueError(path + "<- this does not exists :(")


    #2. végiglapozzuk.
    topic_model = []
    for document in document_array:
        element = dict()
        element['lang'] = document['lang']
        element['url'] = document['url']
        element['text'] = document['text']
        element['id'] = document['id']
        element['label'] = findMostImportantWord(document['text'])
        topic_model.append(element)

    if (os.path.isfile(DynamicTopicsPath)):
        os.remove(DynamicTopicsPath)
    with open(DynamicTopicsPath, 'w') as f:
        json.dump(topic_model, f)

def findMostImportantWord(text):
    return "TODO!!!!"

# topicModelDynamic()
