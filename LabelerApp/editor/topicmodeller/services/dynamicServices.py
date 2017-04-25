# -*- coding: utf-8 -*-
import collections
import json
import os
from collections import defaultdict

import operator

import itertools
from gensim import corpora
from gensim import models

from editor.topicmodeller.utils.consts import linkListPath, linkListDocumentsPath, DynamicTopicsPath, stopwordlist, \
    DynamicDictPath, english_stopwords, DynamicTopicsWordsStatisticsPath
from editor.webcrawler.webcrawler.scripts.dynamic_linklist_parse import parse_dynamic_linklist

__author__ = 'forestg'

# logging bekapcsolása:
import logging

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


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
            formattedLinks.append("http://" + s)

    print(formattedLinks)

    if (os.path.isfile(linkListPath)):
        os.remove(linkListPath)
    with open(linkListPath, 'w') as f:
        json.dump(formattedLinks, f)


def parseWebsitesFromLinkList():
    parse_dynamic_linklist()


def topicModelDynamic():
    # 1. megnyitjuk a dokumentumteret.
    path = linkListDocumentsPath
    if (os.path.exists(path)):
        with open(path) as data_file:
            document_array = json.load(data_file)
    else:
        raise ValueError(path + "<- this does not exists :(")

    # 2. tokenizáljuk, megtisztítjuk a dokumentteret.
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
        .lower().split() if word not in stopwordlist] for document in document_array]
    # 3. megszámoljuk az összes szó előfordulási gyakoriságát
    from collections import defaultdict
    frequencies_dict = defaultdict(int)
    for text in tokenized_documents:
        for token in text:
            frequencies_dict[token] += 1
    # 4. megszűrjük továbbá, azok a szavak amik csak egyszer fordulnak elő, nekünk nem kellenek.
    tokenized_filtered_documents = [[token for token in text if frequencies_dict[token] > 1]
                                    for text in tokenized_documents]
    # 5. Ezen a ponton kész a dokumentumtér tokenizációja. Jöhet a szótár
    dictionary = corpora.Dictionary(tokenized_filtered_documents)
    dictionary.save(DynamicDictPath)

    print("------")
    print("Documents:", tokenized_documents)
    print("Dictionary:", dictionary.token2id)

    # 6. corpus:
    corpus = [dictionary.doc2bow(text) for text in tokenized_documents]
    print("corpus-----")
    print(corpus)

    # 7 tfidf betanítása
    tfidf = models.TfidfModel(corpus)  # step 1 -- initialize a model
    print("tfidf-----")
    print(tfidf)

    # 8. Transzformáljuk a coprus-t
    corpus_tfidf = tfidf[corpus]

    # 7. megvan a súlyozott vektortér, jöhet az LSI kétdimenziós témaátalakítás
    lsi_model_dim2 = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)  # initialize an LSI transformation
    lsi_model_dim4 = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=4)  # initialize an LSI transformation
    lsi_model_dim8 = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=8)  # initialize an LSI transformation
    lsi_model_dim12 = models.LsiModel(corpus_tfidf, id2word=dictionary,
                                      num_topics=12)  # initialize an LSI transformation


    wordStatisticsObject = {
        "models": [
            {
                "name": "dim2",
                "dimension": 2,
                "topics": [
                    {
                        "no": 1,
                        "words": [
                            lsi_model_dim2.show_topic(0)[0][1],
                            lsi_model_dim2.show_topic(0)[1][1],
                            lsi_model_dim2.show_topic(0)[2][1],
                            lsi_model_dim2.show_topic(0)[3][1],
                            lsi_model_dim2.show_topic(0)[4][1],
                        ],
                    },
                    {
                        "no": 2,
                        "words": [
                            lsi_model_dim2.show_topic(1)[0][1],
                            lsi_model_dim2.show_topic(1)[1][1],
                            lsi_model_dim2.show_topic(1)[2][1],
                            lsi_model_dim2.show_topic(1)[3][1],
                            lsi_model_dim2.show_topic(1)[4][1],
                        ]
                    }
                ]
            },
            {
                "name": "dim4",
                "dimension": 4,
                "topics": [
                    {
                        "no": 1,
                        "words": [
                            lsi_model_dim4.show_topic(0)[0][1],
                            lsi_model_dim4.show_topic(0)[1][1],
                            lsi_model_dim4.show_topic(0)[2][1],
                            lsi_model_dim4.show_topic(0)[3][1],
                            lsi_model_dim4.show_topic(0)[4][1],
                        ],
                    },
                    {
                        "no": 2,
                        "words": [
                            lsi_model_dim4.show_topic(1)[0][1],
                            lsi_model_dim4.show_topic(1)[1][1],
                            lsi_model_dim4.show_topic(1)[2][1],
                            lsi_model_dim4.show_topic(1)[3][1],
                            lsi_model_dim4.show_topic(1)[4][1],
                        ]
                    },
                    {
                        "no": 3,
                        "words": [
                            lsi_model_dim4.show_topic(2)[0][1],
                            lsi_model_dim4.show_topic(2)[1][1],
                            lsi_model_dim4.show_topic(2)[2][1],
                            lsi_model_dim4.show_topic(2)[3][1],
                            lsi_model_dim4.show_topic(2)[4][1],
                        ],
                    },
                    {
                        "no": 4,
                        "words": [
                            lsi_model_dim4.show_topic(3)[0][1],
                            lsi_model_dim4.show_topic(3)[1][1],
                            lsi_model_dim4.show_topic(3)[2][1],
                            lsi_model_dim4.show_topic(3)[3][1],
                            lsi_model_dim4.show_topic(3)[4][1],
                        ]
                    }
                ]
            },
            {
                "name": "dim8",
                "dimension": 8,
                "topics": [
                    {
                        "no": 1,
                        "words": [
                            lsi_model_dim8.show_topic(0)[0][1],
                            lsi_model_dim8.show_topic(0)[1][1],
                            lsi_model_dim8.show_topic(0)[2][1],
                            lsi_model_dim8.show_topic(0)[3][1],
                            lsi_model_dim8.show_topic(0)[4][1],
                        ],
                    },
                    {
                        "no": 2,
                        "words": [
                            lsi_model_dim8.show_topic(1)[0][1],
                            lsi_model_dim8.show_topic(1)[1][1],
                            lsi_model_dim8.show_topic(1)[2][1],
                            lsi_model_dim8.show_topic(1)[3][1],
                            lsi_model_dim8.show_topic(1)[4][1],
                        ]
                    },
                    {
                        "no": 3,
                        "words": [
                            lsi_model_dim8.show_topic(2)[0][1],
                            lsi_model_dim8.show_topic(2)[1][1],
                            lsi_model_dim8.show_topic(2)[2][1],
                            lsi_model_dim8.show_topic(2)[3][1],
                            lsi_model_dim8.show_topic(2)[4][1],
                        ],
                    },
                    {
                        "no": 4,
                        "words": [
                            lsi_model_dim8.show_topic(3)[0][1],
                            lsi_model_dim8.show_topic(3)[1][1],
                            lsi_model_dim8.show_topic(3)[2][1],
                            lsi_model_dim8.show_topic(3)[3][1],
                            lsi_model_dim8.show_topic(3)[4][1],
                        ]
                    },

                    {
                        "no": 5,
                        "words": [
                            lsi_model_dim8.show_topic(4)[0][1],
                            lsi_model_dim8.show_topic(4)[1][1],
                            lsi_model_dim8.show_topic(4)[2][1],
                            lsi_model_dim8.show_topic(4)[3][1],
                            lsi_model_dim8.show_topic(4)[4][1],
                        ],
                    },
                    {
                        "no": 6,
                        "words": [
                            lsi_model_dim8.show_topic(5)[0][1],
                            lsi_model_dim8.show_topic(5)[1][1],
                            lsi_model_dim8.show_topic(5)[2][1],
                            lsi_model_dim8.show_topic(5)[3][1],
                            lsi_model_dim8.show_topic(5)[4][1],
                        ]
                    },
                    {
                        "no": 7,
                        "words": [
                            lsi_model_dim8.show_topic(6)[0][1],
                            lsi_model_dim8.show_topic(6)[1][1],
                            lsi_model_dim8.show_topic(6)[2][1],
                            lsi_model_dim8.show_topic(6)[3][1],
                            lsi_model_dim8.show_topic(6)[4][1],
                        ],
                    },
                    {
                        "no": 8,
                        "words": [
                            lsi_model_dim8.show_topic(7)[0][1],
                            lsi_model_dim8.show_topic(7)[1][1],
                            lsi_model_dim8.show_topic(7)[2][1],
                            lsi_model_dim8.show_topic(7)[3][1],
                            lsi_model_dim8.show_topic(7)[4][1],
                        ]
                    }
                ]
            },
            {
                "name": "dim12",
                "dimension": 12,
                "topics": [
                    {
                        "no": 1,
                        "words": [
                            lsi_model_dim12.show_topic(0)[0][1],
                            lsi_model_dim12.show_topic(0)[1][1],
                            lsi_model_dim12.show_topic(0)[2][1],
                            lsi_model_dim12.show_topic(0)[3][1],
                            lsi_model_dim12.show_topic(0)[4][1],
                        ],
                    },
                    {
                        "no": 2,
                        "words": [
                            lsi_model_dim12.show_topic(1)[0][1],
                            lsi_model_dim12.show_topic(1)[1][1],
                            lsi_model_dim12.show_topic(1)[2][1],
                            lsi_model_dim12.show_topic(1)[3][1],
                            lsi_model_dim12.show_topic(1)[4][1],
                        ]
                    },
                    {
                        "no": 3,
                        "words": [
                            lsi_model_dim12.show_topic(2)[0][1],
                            lsi_model_dim12.show_topic(2)[1][1],
                            lsi_model_dim12.show_topic(2)[2][1],
                            lsi_model_dim12.show_topic(2)[3][1],
                            lsi_model_dim12.show_topic(2)[4][1],
                        ],
                    },
                    {
                        "no": 4,
                        "words": [
                            lsi_model_dim12.show_topic(3)[0][1],
                            lsi_model_dim12.show_topic(3)[1][1],
                            lsi_model_dim12.show_topic(3)[2][1],
                            lsi_model_dim12.show_topic(3)[3][1],
                            lsi_model_dim12.show_topic(3)[4][1],
                        ]
                    },
                    {
                        "no": 5,
                        "words": [
                            lsi_model_dim12.show_topic(4)[0][1],
                            lsi_model_dim12.show_topic(4)[1][1],
                            lsi_model_dim12.show_topic(4)[2][1],
                            lsi_model_dim12.show_topic(4)[3][1],
                            lsi_model_dim12.show_topic(4)[4][1],
                        ],
                    },
                    {
                        "no": 6,
                        "words": [
                            lsi_model_dim12.show_topic(5)[0][1],
                            lsi_model_dim12.show_topic(5)[1][1],
                            lsi_model_dim12.show_topic(5)[2][1],
                            lsi_model_dim12.show_topic(5)[3][1],
                            lsi_model_dim12.show_topic(5)[4][1],
                        ]
                    },
                    {
                        "no": 7,
                        "words": [
                            lsi_model_dim12.show_topic(6)[0][1],
                            lsi_model_dim12.show_topic(6)[1][1],
                            lsi_model_dim12.show_topic(6)[2][1],
                            lsi_model_dim12.show_topic(6)[3][1],
                            lsi_model_dim12.show_topic(6)[4][1],
                        ],
                    },
                    {
                        "no": 8,
                        "words": [
                            lsi_model_dim12.show_topic(7)[0][1],
                            lsi_model_dim12.show_topic(7)[1][1],
                            lsi_model_dim12.show_topic(7)[2][1],
                            lsi_model_dim12.show_topic(7)[3][1],
                            lsi_model_dim12.show_topic(7)[4][1],
                        ]
                    },
                    {
                        "no": 9,
                        "words": [
                            lsi_model_dim12.show_topic(8)[0][1],
                            lsi_model_dim12.show_topic(8)[1][1],
                            lsi_model_dim12.show_topic(8)[2][1],
                            lsi_model_dim12.show_topic(8)[3][1],
                            lsi_model_dim12.show_topic(8)[4][1],
                        ],
                    },
                    {
                        "no": 10,
                        "words": [
                            lsi_model_dim12.show_topic(9)[0][1],
                            lsi_model_dim12.show_topic(9)[1][1],
                            lsi_model_dim12.show_topic(9)[2][1],
                            lsi_model_dim12.show_topic(9)[3][1],
                            lsi_model_dim12.show_topic(9)[4][1],
                        ]
                    },
                    {
                        "no": 11,
                        "words": [
                            lsi_model_dim12.show_topic(10)[0][1],
                            lsi_model_dim12.show_topic(10)[1][1],
                            lsi_model_dim12.show_topic(10)[2][1],
                            lsi_model_dim12.show_topic(10)[3][1],
                            lsi_model_dim12.show_topic(10)[4][1],
                        ],
                    },
                    {
                        "no": 12,
                        "words": [
                            lsi_model_dim12.show_topic(11)[0][1],
                            lsi_model_dim12.show_topic(11)[1][1],
                            lsi_model_dim12.show_topic(11)[2][1],
                            lsi_model_dim12.show_topic(11)[3][1],
                            lsi_model_dim12.show_topic(11)[4][1],
                        ]
                    },
                ]
            },
        ]
    }


    corpus_lsi_2 = lsi_model_dim2[corpus_tfidf]
    corpus_lsi_4 = lsi_model_dim4[corpus_tfidf]
    corpus_lsi_8 = lsi_model_dim8[corpus_tfidf]
    corpus_lsi_12 = lsi_model_dim12[corpus_tfidf]

    from operator import itemgetter

    corpus_category_lsi2 = []
    corpus_category_lsi4 = []
    corpus_category_lsi8 = []
    corpus_category_lsi12 = []

    for index,doc in enumerate(corpus_lsi_2):
        max_value_index = max(doc, key=itemgetter(1))[0]
        corpus_category_lsi2.append(max_value_index)
    for index,doc in enumerate(corpus_lsi_4):
        max_value_index = max(doc, key=itemgetter(1))[0]
        corpus_category_lsi4.append(max_value_index)
    for index,doc in enumerate(corpus_lsi_8):
        max_value_index = max(doc, key=itemgetter(1))[0]
        corpus_category_lsi8.append(max_value_index)
    for index,doc in enumerate(corpus_lsi_12):
        max_value_index = max(doc, key=itemgetter(1))[0]
        corpus_category_lsi12.append(max_value_index)



    if (os.path.isfile(DynamicTopicsWordsStatisticsPath)):
        os.remove(DynamicTopicsWordsStatisticsPath)
    with open(DynamicTopicsWordsStatisticsPath, 'w') as f:
        json.dump(wordStatisticsObject, f)

    # 3. TopicModel fájl lementése
    topic_model = []
    for index,document in enumerate(document_array):
        element = dict()
        element['lang'] = document['lang']
        element['url'] = document['url']
        element['text'] = document['text']
        element['id'] = document['id']
        element['topImportantWord'] = findMostImportantWord(document['text'])
        element['mostFrequentWord'] = getMostFrequentWord(document['text'])
        element['topic2'] = corpus_category_lsi2[index]
        element['topic4'] = corpus_category_lsi4[index]
        element['topic8'] = corpus_category_lsi8[index]
        element['topic12'] = corpus_category_lsi12[index]
        topic_model.append(element)

    if (os.path.isfile(DynamicTopicsPath)):
        os.remove(DynamicTopicsPath)
    with open(DynamicTopicsPath, 'w') as f:
        json.dump(topic_model, f)


def findMostImportantWord(text):
    return "TODO!!!!"


def findTopic(text):
    return "TODO!!!!"


def getMostFrequentWord(text):
    from sklearn.feature_extraction import stop_words
    frequencies_dict = defaultdict(int)
    tokenized_text = [word for word in text \
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
        .lower().split() if word not in itertools.chain(english_stopwords, stopwordlist)]

    for word in tokenized_text:
        frequencies_dict[word] += 1

    # http://stackoverflow.com/questions/268272/getting-key-with-maximum-value-in-dictionary
    return (max(frequencies_dict.iteritems(), key=operator.itemgetter(1))[0])


topicModelDynamic()
# getMostFrequentWord(u'ablak zsiráf ablak megint, és egy kicsiz zsiráf zsiráf zsiráf is.')
