# -*- coding: utf-8 -*-
import json
import os

from gensim import corpora

from editor.topicmodeller.utils.consts import wikiDictionaryPath, stopwordlist, WikiFrequenciesPath, WikiDictionaryPath, \
    WikiDocumentsPath, WikiTopicsPath2

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

def topic_model_wiki_hu():
    from gensim import corpora, models, similarities

    # 1. Szótár betöltése
    dictPath = WikiDictionaryPath
    if (os.path.exists(dictPath)):
        with open(dictPath) as data_file:
            dictionary = corpora.Dictionary.load(dictPath)
    else:
        raise ValueError(dictPath + "<- dict. path :(")

    # 2. corpus betöltése

    path = WikiDocumentsPath
    if (os.path.isfile(path)):
        with open(path) as data_file:
            document_list = json.load(data_file)
    else:
        raise ValueError(path + "<- this does not exists :(")

    print("document----")
    print("size: ", len(document_list))

    # todo: akár refaktorozhatnád is...
    tokenized_documents = [[word for word in document.get('text') \
        .replace(",", " ") \
        .replace(".", " ") \
        .replace("!", " ") \
        .replace(";", " ") \
        .replace("\"", " ") \
        .replace("(", " ") \
        .replace(")", " ") \
        .replace(":", " ") \
        .replace("?", " ") \
        .replace("'", " ") \
        .lower().split() if word not in stopwordlist] for document in document_list]


    corpus = [dictionary.doc2bow(text) for text in tokenized_documents]

    tfidf = models.TfidfModel(corpus)  # step 1 -- initialize a model

    corpus_tfidf = tfidf[corpus]

    lsi_model_dim2 = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)  # initialize an LSI transformation

    print("LSI_MODEL_KÉTDÉ-----")
    print(lsi_model_dim2)
    print(lsi_model_dim2.show_topic(0))
    print(lsi_model_dim2.show_topic(1))

    # lsi_topics_dim2 = {
    #     lsi_model_dim2.show_topic(0),
    #     lsi_model_dim2.show_topic(1)
    # }

    print("---")


    lsi_topics_dim2 = {
        1:
            [
                lsi_model_dim2.show_topic(0)[0][1],
                lsi_model_dim2.show_topic(0)[1][1],
                lsi_model_dim2.show_topic(0)[2][1],
                lsi_model_dim2.show_topic(0)[3][1],
                lsi_model_dim2.show_topic(0)[4][1],
            ],
        2:
            [
                lsi_model_dim2.show_topic(1)[0][1],
                lsi_model_dim2.show_topic(1)[1][1],
                lsi_model_dim2.show_topic(1)[2][1],
                lsi_model_dim2.show_topic(1)[3][1],
                lsi_model_dim2.show_topic(1)[4][1],
            ]
    }

    print(lsi_topics_dim2)


    print("counting words: -----")
    topic1WordCountOnDocuments= [0] * tokenized_documents.__len__()
    for word in lsi_topics_dim2[1]:
        for index, text in enumerate(tokenized_documents):
            topic1WordCountOnDocuments[index] += tokenized_documents[index].count(word)
    topic2WordCountOnDocuments= [0] * tokenized_documents.__len__()
    for word in lsi_topics_dim2[2]:
        for index, text in enumerate(tokenized_documents):
            topic2WordCountOnDocuments[index] += tokenized_documents[index].count(word)


    maxValue = max(topic1WordCountOnDocuments)
    indexOfMaxValue = topic1WordCountOnDocuments.index(maxValue)
    document = document_list[indexOfMaxValue]
    print("Winner today:", document)

    lsi_topics_dim2[1].append(document)

    maxValue = max(topic2WordCountOnDocuments)
    indexOfMaxValue = topic2WordCountOnDocuments.index(maxValue)
    document = document_list[indexOfMaxValue]
    print("Winner 2 today:", document)
    lsi_topics_dim2[2].append(document)






    if (os.path.isfile(WikiTopicsPath2)):
        os.remove(WikiTopicsPath2)
    with open(WikiTopicsPath2, 'w') as f:
        json.dump(lsi_topics_dim2, f, sort_keys=True)


# topic_model_wiki_hu()
