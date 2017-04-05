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

def tutorial2():
    from gensim import corpora, models, similarities
    if (os.path.exists("./../data/deerwester.dict")):
        dictionary = corpora.Dictionary.load('./../data/deerwester.dict')
        print(dictionary)
        corpus = corpora.MmCorpus('./../data/deerwester.mm')
        print(corpus)
        print("Used files generated from first tutorial")
    else:
       print("Please run first tutorial to generate data set")

    tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model

    doc_bow = [(0, 1), (1, 1)]
    print(tfidf[doc_bow]) # step 2 -- use the model to transform vectors

    #for the whole corpus:
    corpus_tfidf = tfidf[corpus]
    for doc in corpus_tfidf:
        print(doc)

    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2) # initialize an LSI transformation
    corpus_lsi = lsi[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi
    lsi.print_topics(2)

    for doc in corpus_lsi: # both bow->tfidf and tfidf->lsi transformations are actually executed here, on the fly
        print(doc)



tutorial2()
