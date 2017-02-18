# -*- coding: utf-8 -*-
__author__ = 'forestg'
from gensim import corpora, models, similarities
import os.path
import pickle
# logging bekapcsolása:
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

def yieldLabels(article,label):

    stopwordlist = (u'a az egy be ki le fel meg el át rá ide oda szét össze vissza de hát és vagy hogy van lesz volt csak'+
               u'nem igen mint én te õ mi ti õk ön ide volt ő ők ahogy ahol aki akik akkor alatt által általában '+
               u'amely amelyek amelyekben amelyeket amelyet amelynek ami amit amolyan amíg amikor abban ahhoz annak '+
               u'arra arról azok azon azt azzal azért aztán azután azonban bár belül benne cikk cikkek cikkeket e '+
               u'eddig egész egyes egyetlen egyéb egyik egyre ekkor elég ellen elő először előtt első éppen ebben '+
               u'ehhez emilyen ennek erre ez ezt ezek ezen ezzel ezért felé hanem hiszen hogyan így illetve ill. ill '+
               u'ilyen ilyenkor ismét itt jó jól jobban kell kellett keresztül keressünk kívül között közül legalább '+
               u'lehet lehetett legyen lenne lenni lett maga magát majd már más másik még mellett mert mely melyek '+
               u'mit míg miért milyen mikor minden mindent mindenki mindig mintha mivel most nagy nagyobb nagyon ne '+
               u'néha nekem neki néhány nélkül nincs olyan ott őket pedig persze s saját sem semmi sok sokat sokkal '+
               u'számára szemben szerint szinte talán tehát teljes tovább továbbá több úgy ugyanis új újabb újra után '+
               u'utána utolsó vagyis valaki valami valamint való vagyok vannak voltam voltak voltunk vele viszont '+
               u'volna alá ha is ad szerző helyett amúgy főleg os es szerintem oka hozzászólás soha hozzászólások '+
               u'száma kategória feladva komment szia hello üdv')


    dictionaryPath = '/tmp/onlab/dictionary' # -- I do not use this at the moment for anything.
    corpusPath = "/tmp/onlab/corpus" #  -- I do not use this at the moment for anything.
    documentsPath = '/tmp/onlab/labelerAppDocuments'
    labelsPath = '/tmp/onlab/labelerAppLabels'
    documents_list = []
    labels_list = []

    print("Initializing... given strings:")
    print(article)
    print(label)
    print("IO actions...")

    #1. Dokumentumok megnyitása.
    if (os.path.isfile(documentsPath)):
        print("Opening stored documents list...");
        with open(labelsPath,'rb') as f:
            labels_list = pickle.load(f)
        with open(documentsPath, 'rb') as f:
            documents_list = pickle.load(f)
        print(documents_list)
    else:
        print("Creating new documents list fie...");
        documents_list.append("dummy article");
        labels_list.append("dummy labels")
        print(documents_list)

    #2. Tokenize and get rid of stop words.
    print("--tokenized stopword-filtered:")
    tokenizalt = [[word for word in document.lower().split() if word not in stopwordlist]
             for document in documents_list]
    print(tokenizalt)

    #2.5 TODO - insert filtering words that only occures only once. Do I need it?

    #3. create dictionary.
    dictionary = corpora.Dictionary(tokenizalt)
    # dictionary.save(dictionaryPath)
    print("-- Dictionary:")
    print(dictionary)
    print(dictionary.token2id)

    #4. transform it to vector space
    print("--The corpus transformed:")
    corpus = [dictionary.doc2bow(text) for text in tokenizalt]
    # corpora.MmCorpus.serialize(corpusPath, corpus) # store to disk, for later use
    print(corpus)

    #5. Generate TFIDF model - don't need it now
    # tfidf = models.TfidfModel(corpus)

    #6 generate 2 dimensional space
    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)

    #7. Now work on the given text, to find the closes neighbor.
    print("--paramter text:")
    print(article)
    vec_bow = dictionary.doc2bow(article.lower().split())
    print("in vec_bow:")
    print(vec_bow)
    vec_lsi = lsi[vec_bow] # convert the query to LSI space
    print("in lsi_vec:")
    print(vec_lsi)

    #8 generate similarities index
    index = similarities.MatrixSimilarity(lsi[corpus])

    #9. compare the two documents.
    sims = index[vec_lsi] # perform a similarity query against the corpus
    print(list(enumerate(sims))) # print (document_number, document_similarity) 2-tuples
    print("----")
    # eredmény értelmezése: -1 és 1 között a dokumentumok közül melyik mennyire volt hasonló hozzá.

    #10. get it sorted by the similarity score
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    print("--- Similarities:")
    print(sims)

    labels = label
    #labels += " " + documents_list[sims[0][0]] # to get the documents instead (for debug)

    newLabel =  labels_list[sims[0][0]]
    labels += u" " + newLabel # this gets the number of the highest scored document

    #11. Storing new datas on the disk.
    documents_list.append(article)
    labels_list.append(label)
    with open(documentsPath, 'wb') as f:
        pickle.dump(documents_list, f)
    with open(labelsPath, 'wb') as f:
        pickle.dump(labels_list, f)
    print("Document list stored.");
    print("-------------------------------------------------------Return value:")

    return labels

# Néhány dummy data próbálgatásnak. Elvilkeg működik
#print (yieldLabels("Ablak Rogán Rogln azasdasdasd Wikc","ElsőDefLabel"))
#print (yieldLabels("Orbán Viktor együtt focizott a Felcsúti kedves bácsikkal, Fidesz pólóban","MásodikDefLabel"))
#print (yieldLabels("Rogán Antal szerint a Fidesz legfőbb feladata, hogy foci stadionokat építsen","HarmadikDefLabel"))
#print (yieldLabels("Senki nem szereti már a facebookot - állapították meg angol kutatók","NegyedikDefLabel"))
#print (yieldLabels( "Bill Clinton újra indul fidesz az Ameriakai elnökválasztásért meg Fidesz.","ÖtödikDefLabel"))

