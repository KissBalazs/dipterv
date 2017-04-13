# -*- coding: utf-8 -*-
import json
import os

from gensim import corpora

from editor.topicmodeller.utils.consts import wikiDictionaryPath, stopwordlist, WikiFrequenciesPath, WikiDictionaryPath, \
    WikiDocumentsPath

__author__ = 'forestg'

# logging bekapcsolása:
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def create_dictionary_wiki(): #todo: ezt lehetne rafactorozni
    dir = os.path.dirname(__file__)
    path = os.path.join(dir, wikiDictionaryPath)

    if (os.path.isfile(path)):
        os.remove(path)

    path = WikiDocumentsPath
    if (os.path.isfile(path)):
        with open(path) as data_file:
            document_list = json.load(data_file)
    else:
        raise ValueError(path+"<- this does not exists :(")

    # # print("dokumentumok:", document_list)
    #1. Betöltjük a dokumentumokat, feldaraboljuk őket, és kiszedjük a stop-szavakat.
    tokenized_documents = [[word for word in document.get('text')       \
                                                     .replace(","," ")  \
                                                     .replace("."," ") \
                                                     .replace("!"," ")  \
                                                     .replace(";"," ")  \
                                                     .replace("\""," ") \
                                                     .replace("(", " ") \
                                                     .replace(")", " ") \
                                                     .replace(":", " ") \
                                                     .replace("?", " ") \
                                                     .replace("'", " ") \
                                                     .lower().split() if word not in stopwordlist] for document in document_list]

    # tokenized_documents = [[word for word in document.get('text').lower().split() if word not in stopwordlist]
    #          for document in document_list]

    print("tokenizált:----")
    print(tokenized_documents)

    from collections import defaultdict
    frequency = defaultdict(int)
    for text in tokenized_documents:
        for token in text:
            frequency[token] += 1

    tokenized_filtered_documents = [[token for token in text if frequency[token] > 1]
                                    for text in tokenized_documents]

    print("frequency----")
    print(frequency)
    if (os.path.isfile(WikiFrequenciesPath)):
        os.remove(WikiFrequenciesPath)
    with open(WikiFrequenciesPath, 'w') as f:
        json.dump(frequency, f)

    dictionary = corpora.Dictionary(tokenized_filtered_documents)
    dictionary.save(WikiDictionaryPath)

create_dictionary_wiki()
