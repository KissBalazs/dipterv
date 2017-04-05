# -*- coding: utf-8 -*-
from gensim import corpora, models, similarities


def yieldLabels(text,labels):
    cikkek = ["Orbán Viktor együtt focizott a Felcsúti kedves bácsikkal, Fidesz pólóban",
              "Rogán Antal szerint a Fidesz legfőbb feladata, hogy foci stadionokat építsen",
              "Senki nem szereti már a facebookot - állapították meg angol kutatók"
              "Bill Clinton újra indul az Ameriakai elnökválasztásért."]
    cimkek = ["Orbán Viktor, Fidesz",
              "Rogán Antal, Fidesz, Stadion",
              "Angol tudósok, facebook, média",
              "Bill Clinton, USA, elnökválasztás"]

    stopwordlist = ["a hogy már meg az"]

    # teokenizáljuk a szövegeket és tegyük be a texts-be, ha nem szerepel a stopszótárban
    # hogy is működik ez az egyenlőség? "Külső" iterálás: document (sorok) megy körbe. Ezen belül
    # egy word (szavak) ami a document(sor) splitjei, és csak akkor,
    # ha nincs benne a stoplist-ben.
    print("--tokenized stopword-filtered:-----")
    tokenizalt = [[word for word in document.lower().split() if word not in stopwordlist]
             for document in cikkek]
    print(tokenizalt)

    # kiszedüjük azokat a szavakat, amik csak egyszer fordulnak elő
    #print("--only multiple occurrances:-------")
    #all_tokens = sum(texts, [])
    #tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
    #texts = [[word for word in text if word not in tokens_once]
    #         for text in texts]
    #print(texts)

    #most jöhet a vektorizálás. Ehhez bag-of-wordest fogunk haználni (hányszor szerepel 1-1 szó
    # TODO - új text hozzáadása a dictionary-hez.
    dictionary = corpora.Dictionary(tokenizalt)
    # le is lehet menteni fájlba like this
    dictionary.save('/tmp/myexperiemnt.dict')
    print("--dictionary:-------")
    print(dictionary)

    # kész a vektorizálás - minden szóhoz egy saját integert rendeltünk. meg is nézhetjük:
    print(dictionary.token2id)

    #most pedig nézzük az egész corpust!
    print("--The corpus transformed:----------")
    corpus = [dictionary.doc2bow(text) for text in tokenizalt]
    corpora.MmCorpus.serialize('/tmp/myexperiemnt.mm', corpus) # store to disk, for later use
    print(corpus)

    # Transzformáció inicializálása
    tfidf = models.TfidfModel(corpus)

    # most létrehozunk egy kétdimenziós LSI teret:
    lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)

    # Szeretnénk az adott kifejezéshez "legközelebb-állás" szerint rendezni a corpusunkat.
    doc = labels
    vec_bow = dictionary.doc2bow(doc.lower().split())
    vec_lsi = lsi[vec_bow] # convert the query to LSI space
    print(vec_lsi)
    print("----")

    # Ahhoz, hogy megtehessük a rendezést, indexet kell létrehoznunk.
    index = similarities.MatrixSimilarity(lsi[corpus])
    # És most pedig jöjjön két dokumentum összehasonlítása:
    sims = index[vec_lsi] # perform a similarity query against the corpus
    print(list(enumerate(sims))) # print (document_number, document_similarity) 2-tuples
    print("----")
    # eredmény értelmezése: -1 és 1 között a dokumentumok közül melyik mennyire volt hasonló hozzá.

    # Kis pythonos ügyeskedéssel sorrendbe állítjuk, és megadjuk a végső választ az eredeti query-re:
    sims = sorted(enumerate(sims), key=lambda item: -item[1])
    print(sims)

    # végül az eredmény:
    # print(cimkek[1])
    # print(cimkek[sims[0,0]])
     # print(cimkek[sims[0][0]])cimkek[sims[0][0]] + " " + cimkek[sims[0][1]] + " " + cimkek[sims[0][2]]
    labels += " " + cimkek[sims[0][0]].decode('utf-8')

    return labels

# print(yieldLabels("facebookot egy szar", "elso_label"))
