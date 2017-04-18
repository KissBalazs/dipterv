# -*- coding: utf-8 -*-
import json
import os
from pprint import pprint

import operator
from gensim import corpora

from editor.topicmodeller.utils.consts import indexDictionaryPath, stopwordlist, IndexDocumentsPath, \
    IndexDictionaryPath, \
    IndexFrequenciesPath, IndexTopicsPath2

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
        raise ValueError(path + "<- this does not exists :(")

    # print("dokumentumok:", document_list)
    # 1. Betöltjük a dokumentumokat, feldaraboljuk őket, és kiszedjük a stop-szavakat.
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

    print("tokenizált:----")
    print(tokenized_documents)

    # todo: whitespace-re cserél le a pontot és a vesszőt mindehol

    # 2. megszűrjük továbbá, azok a szavak amik csak egyszer fordulnak elő, nekünk nem kellenek.
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

    # 3. Ezen a ponton kész a dokumentumtér tokenizációja. Jöhet a szótár
    dictionary = corpora.Dictionary(tokenized_filtered_documents)
    dictionary.save(IndexDictionaryPath)
    # print("token2id----")
    # print(dictionary.token2id)
    # print("doc2bow------")
    # print(dictionary.doc2bow(dictionary))
    # sorted_x = sorted(dictionary.token2id.items(), key=operator.itemgetter(1))
    # print(sorted_x)


# create_dictionary_index()

def topic_model_index_hu():
    from gensim import corpora, models, similarities

    # 1. Szótár betöltése
    dictPath = IndexDictionaryPath
    if (os.path.exists(dictPath)):
        with open(dictPath) as data_file:
            dictionary = corpora.Dictionary.load(dictPath)
    else:
        raise ValueError(dictPath + "<- dict. path :(")

    # 2. corpus betöltése

    path = IndexDocumentsPath
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





    # ---------------------------- TUTORIALOS BETANÍTÓ ---------------------------------------
    # documents = ["Human machine interface for lab abc computer applications",
    #              "A survey of user opinion of computer system response time",
    #              "The EPS user interface management system",
    #              "System and human system engineering testing of EPS",
    #              "Relation of user perceived response time to error measurement",
    #              "The generation of random binary unordered trees",
    #              "The intersection graph of paths in trees",
    #              "Graph minors IV Widths of trees and well quasi ordering",
    #              "Graph minors A survey"]
    #
    # # remove common words and tokenize
    # stoplist = set('for a of the and to in'.split())
    # texts = [[word for word in document.lower().split() if word not in stoplist]
    #          for document in documents]
    #
    # # remove words that appear only once
    # from collections import defaultdict
    # frequency = defaultdict(int)
    # for text in texts:
    #     for token in text:
    #         frequency[token] += 1
    #
    # tokenized_documents = [[token for token in text if frequency[token] > 1]
    #          for text in texts]
    #
    # from pprint import pprint  # pretty-printer
    # pprint(texts)
    #
    # dictionary = corpora.Dictionary(texts)
    # ---------------------------- TUTORIALOS BETANÍTÓ ---------------------------------------

    print("tokenizált:----")
    print(tokenized_documents)
    print("elemszám:", tokenized_documents.__len__())

    # 3 ezen a ponton tudjuk, hogy a lementett dokumentumtér indexei megegyeznek a most megnyitott dokumentumtér indexjeivel. Erog majd amellé kell beszúrni

    print("dict. token2id-----")
    print(dictionary.token2id)

    # 4. tokenizált dokumentum vektor megjelenítése

    corpus = [dictionary.doc2bow(text) for text in tokenized_documents]
    print("corpus-----")
    print(corpus)
    # print(u'b\xedr\xf3s\xe1g') - letesztelve, működik eddig

    # 5 Jöhet a tfidf betanítása
    tfidf = models.TfidfModel(corpus)  # step 1 -- initialize a model
    print("tfidf-----")
    print(tfidf)

    # 6. Transzformáljuk a coprus-t
    corpus_tfidf = tfidf[corpus]
    # for doc in corpus_tfidf:
    #     print(doc)





    # 7. megvan a súlyozott vektortér, jöhet az LSI kétdimenziós témaátalakítás todo: legyen több diemnzió
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
    # lsiTopicsWith2D = lsi_model_dim2.print_topics(2)
    # lsi_model_dim4 = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=4) # initialize an LSI transformation
    # lsiTopicsWith4D = lsi_model_dim4.print_topics(4)
    # lsi_model_dim8 = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=8) # initialize an LSI transformation
    # lsiTopicsWith8D = lsi_model_dim8.print_topics(8)

    # #8 tádá - a két topicot kiírja és a hozzá kapcsolódó szavakat
    #

    #
    # if (os.path.isfile(IndexTopicsPath4)):
    #     os.remove(IndexTopicsPath4)
    # with open(IndexTopicsPath4, 'w') as f:
    #     json.dump(lsiTopicsWith4D, f)
    #
    # if (os.path.isfile(IndexTopicsPath8)):
    #     os.remove(IndexTopicsPath8)
    # with open(IndexTopicsPath8, 'w') as f:
    #     json.dump(lsiTopicsWith8D, f)


    # nézzük meg a legközelebbi dokumentumot
    corpus_lsi_dim2 = lsi_model_dim2[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi




    # -----------------------------------------------
    # --------- TFIDF + LSI bukása ------------------
    # -----------------------------------------------
    # print("corpus_lsi_dim2----")
    # print (corpus_lsi_dim2)
    # print("docs-----")
    # lowest_value_0 = 0.0
    # lowest_value_1 = 0.0
    # lowest_index_0 = 0
    # lowest_index_1 = 0
    # highest_value_0 = 0.0
    # highest_value_1 = 0.0
    # highest_index_0 = 0
    # highest_index_1 = 0
    #
    # print("---corpus-----")
    #
    # for index, doc in enumerate(corpus_lsi_dim2):
    #     print(index, doc)        # print("val:", doc[0][1])
    #     if(doc):
    #         if(doc[0][1]>highest_value_0):
    #             highest_value_0 = doc[0][1]
    #             highest_index_0 = index
    #         if(doc[0][1]<lowest_value_0):
    #             lowest_value_0 = doc[0][1]
    #             lowest_index_0 = index
    #
    #         if(doc[1][1]>highest_value_1 and doc[1][1]>0.8):
    #             highest_value_1 = doc[1][1]
    #             highest_index_1 = index
    #         if(doc[1][1]<lowest_value_1):
    #             lowest_value_1 = doc[1][1]
    #             lowest_index_1 = index
    #
    # print("Témakörök:-----")
    # print("topic 1 szavak:", lsi_topics_dim2[1])
    # print("topic 2 szavak:", lsi_topics_dim2[2])
    #
    # print("Eredmények:------")
    # print("topic 0, lowest:",lowest_value_0, lowest_index_0, document_list[lowest_index_0].get("text"))
    # print("topic 0, highest:", highest_value_0, highest_index_0, document_list[highest_index_0].get("text"))
    #
    # print("topic 1, lowest:",lowest_value_1, lowest_index_1, document_list[lowest_index_1].get("text"))
    # print("topic 1, highest:", highest_value_1, highest_index_1, document_list[highest_index_1].get("text"))
    #
    # winnerDocumentForTopic1 = document_list[highest_index_1]
    # winnerDocumentForTopic2 = document_list[lowest_index_1]
    #
    # lsi_topics_dim2[1].append(winnerDocumentForTopic1)
    # lsi_topics_dim2[2].append(winnerDocumentForTopic2)
    #
    # print("tosave:", lsi_topics_dim2)




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






    if (os.path.isfile(IndexTopicsPath2)):
        os.remove(IndexTopicsPath2)
    with open(IndexTopicsPath2, 'w') as f:
        json.dump(lsi_topics_dim2, f, sort_keys=True)


# topic_model_index_hu()

#  finomhangolás lépései:
# 1. kütöttem egy csomó felesleges blogot
# 2. kiütöttem a hírfolyamot, mert nem lhet crawlorni
# 3. kiszedtem a kiugróan jól ileszkedő egykarakteres sövegektt, és a nagyon nagyon hosszú cikkeket, pl totalcarosok.
# 4. levojuk a tanulságot: 1. néha hülye témák jönnek ki. 2. mindig másfelé mutatnak a vektorok.

# 5. helyette milye algoritmust használok? -> legfontosabb szavak előfordulási gyakorisága...
