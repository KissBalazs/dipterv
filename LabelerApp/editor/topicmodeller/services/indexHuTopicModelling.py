# -*- coding: utf-8 -*-
import json
import os
from pprint import pprint

import operator
from gensim import corpora

from editor.topicmodeller.utils.consts import indexDictionaryPath, stopwordlist, IndexDocumentsPath, IndexDictionaryPath, \
    IndexFrequenciesPath

__author__ = 'forestg'

# logging bekapcsolása:
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def create_dictionary_index():
    dir = os.path.dirname(__file__)
    path = os.path.join(dir, indexDictionaryPath)

    if (os.path.isfile(path)):
        os.remove(path)

    path = IndexDocumentsPath
    if (os.path.isfile(path)):
        with open(path) as data_file:
            document_list = json.load(data_file)
    else:
        raise ValueError(path+"<- this does not exists :(")

    # print("dokumentumok:", document_list)
    #1. Betöltjük a dokumentumokat, feldaraboljuk őket, és kiszedjük a stop-szavakat.
    tokenized_documents = [[word for word in document.get('text').lower().split() if word not in stopwordlist]
             for document in document_list]

    print("tokenizált:----")
    print(tokenized_documents)

    #todo: whitespace-re cserél le a pontot és a vesszőt mindehol

    #2. megszűrjük továbbá, azok a szavak amik csak egyszer fordulnak elő, nekünk nem kellenek.
    from collections import defaultdict
    frequency = defaultdict(int)
    for text in tokenized_documents:
        for token in text:
            frequency[token] += 1



    tokenized_filtered_documents = [[token for token in text if frequency[token] > 1]
                                    for text in tokenized_documents]

    print("frequency----")
    print(frequency)
    if (os.path.isfile(IndexFrequenciesPath)):
        os.remove(IndexFrequenciesPath)
    with open(IndexFrequenciesPath, 'w') as f:
        json.dump(frequency, f)



    # print("filterezett:----")
    # print(tokenized_filtered_documents)
    #
    # print("dokumentumtér mérete", tokenized_documents.__sizeof__())
    # print("szűretlen mérete:", tokenized_documents[0].__sizeof__())
    # print("Szűrt mérete:", tokenized_filtered_documents[0].__sizeof__())

    #3. Ezen a ponton kész a dokumentumtér tokenizációja. Jöhet a szótár
    dictionary = corpora.Dictionary(tokenized_filtered_documents)
    dictionary.save(IndexDictionaryPath)
    # print("token2id----")
    # print(dictionary.token2id)
    # print("doc2bow------")
    # print(dictionary.doc2bow(dictionary))
    # sorted_x = sorted(dictionary.token2id.items(), key=operator.itemgetter(1))
    # print(sorted_x)

create_dictionary_index()
