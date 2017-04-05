# -*- coding: utf-8 -*-
__author__ = 'forestg'
from gensim import corpora, models, similarities
import os.path
import pickle
import sys
from pprint import pprint  # pretty-printer


# logging bekapcsolása:
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)



def tutorial():
    print("Tutorial started")

    documents = ["Human machine interface for lab abc computer applications",
              "A survey of user opinion of computer system response time",
              "The EPS user interface management system",
              "System and human system engineering testing of EPS",
              "Relation of user perceived response time to error measurement",
              "The generation of random binary unordered trees",
              "The intersection graph of paths in trees",
              "Graph minors IV Widths of trees and well quasi ordering",
              "Graph minors A survey"]

    # remove common words and tokenize
    stoplist = set('for a of the and to in'.split())
    texts = [[word for word in document.lower().split() if word not in stoplist]
             for document in documents]

    # remove words that appear only once - todo nekem ez kell?
    from collections import defaultdict
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    texts = [[token for token in text if frequency[token] > 1] for text in texts]

    pprint(texts)

    dictionary = corpora.Dictionary(texts)
    dictionary.save('./../data/deerwester.dict')  # store the dictionary, for future reference
    print("dictionary:", dictionary)
    print("Tokne2id:", dictionary.token2id)

    #to vector
    new_doc = "Human computer interaction"
    new_vec = dictionary.doc2bow(new_doc.lower().split())
    print(new_vec)  # the word "interaction" does not appear in the dictionary and is ignored

    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('./../data/deerwester.mm', corpus)  # store to disk, for later use
    for c in corpus:
        print(c)







# actually starting the tutorial
tutorial()
