# -*- coding: utf-8 -*-
__author__ = 'forestg'

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
               u'száma kategória feladva komment szia hello üdv - is, , - volt, is. van, kis, ki, meg, meg. ki. után, '+
               u'egész – miatt óta túl ráadásul esetleg végül 	. ')

english_stopwords = (
    "a", "about", "above", "across", "after", "afterwards", "again", "against",
    "all", "almost", "alone", "along", "already", "also", "although", "always",
    "am", "among", "amongst", "amoungst", "amount", "an", "and", "another",
    "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are",
    "around", "as", "at", "back", "be", "became", "because", "become",
    "becomes", "becoming", "been", "before", "beforehand", "behind", "being",
    "below", "beside", "besides", "between", "beyond", "bill", "both",
    "bottom", "but", "by", "call", "can", "cannot", "cant", "co", "con",
    "could", "couldnt", "cry", "de", "describe", "detail", "do", "done",
    "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else",
    "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone",
    "everything", "everywhere", "except", "few", "fifteen", "fifty", "fill",
    "find", "fire", "first", "five", "for", "former", "formerly", "forty",
    "found", "four", "from", "front", "full", "further", "get", "give", "go",
    "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter",
    "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his",
    "how", "however", "hundred", "i", "ie", "if", "in", "inc", "indeed",
    "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter",
    "latterly", "least", "less", "ltd", "made", "many", "may", "me",
    "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly",
    "move", "much", "must", "my", "myself", "name", "namely", "neither",
    "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone",
    "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on",
    "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our",
    "ours", "ourselves", "out", "over", "own", "part", "per", "perhaps",
    "please", "put", "rather", "re", "same", "see", "seem", "seemed",
    "seeming", "seems", "serious", "several", "she", "should", "show", "side",
    "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone",
    "something", "sometime", "sometimes", "somewhere", "still", "such",
    "system", "take", "ten", "than", "that", "the", "their", "them",
    "themselves", "then", "thence", "there", "thereafter", "thereby",
    "therefore", "therein", "thereupon", "these", "they", "thick", "thin",
    "third", "this", "those", "though", "three", "through", "throughout",
    "thru", "thus", "to", "together", "too", "top", "toward", "towards",
    "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us",
    "very", "via", "was", "we", "well", "were", "what", "whatever", "when",
    "whence", "whenever", "where", "whereafter", "whereas", "whereby",
    "wherein", "whereupon", "wherever", "whether", "which", "while", "whither",
    "who", "whoever", "whole", "whom", "whose", "why", "will", "with",
    "within", "without", "would", "yet", "you", "your", "yours", "yourself",
    "yourselves")

indexDictionaryPath = '../documents/IndexDictionary'
wikiDictionaryPath = '../documents/WikiDictionary' # todo: ezek kellenek?

IndexDocumentsPath = "/home/forestg/projects/dipterv/LabelerApp/data/index.json"
IndexDictionaryPath = "/home/forestg/projects/dipterv/LabelerApp/editor/topicmodeller/documents/indexDictionary.dict"
IndexFrequenciesPath = "/home/forestg/projects/dipterv/LabelerApp/editor/topicmodeller/documents/indexFrequency"
IndexTopicsPath2 = "/home/forestg/projects/dipterv/LabelerApp/editor/topicmodeller/documents/indexTopics2.json"

WikiDocumentsPath = "/home/forestg/projects/dipterv/LabelerApp/data/wiki.json"
WikiDictionaryPath = "/home/forestg/projects/dipterv/LabelerApp/editor/topicmodeller/documents/wikiDictionary.dict"
WikiFrequenciesPath = "/home/forestg/projects/dipterv/LabelerApp/editor/topicmodeller/documents/wikiFrequency"
WikiTopicsPath2 = "/home/forestg/projects/dipterv/LabelerApp/editor/topicmodeller/documents/wikiTopics2.json"

linkListPath = "/home/forestg/projects/dipterv/LabelerApp/data/linkLinst.json"
linkListDocumentsPath = "/home/forestg/projects/dipterv/LabelerApp/editor/topicmodeller/documents/dynamicDocuments.json"
DynamicTopicsPath = "/home/forestg/projects/dipterv/LabelerApp/editor/topicmodeller/documents/dynamicTopics.json"
DynamicTopicsWordsStatisticsPath = "/home/forestg/projects/dipterv/LabelerApp/editor/topicmodeller/documents/dynamicTopicsWordsStatisticsPath.json"
DynamicDictPath = "/home/forestg/projects/dipterv/LabelerApp/editor/topicmodeller/documents/dynamicDictionary.dict"

DynamicDictPathEng = "/home/forestg/projects/dipterv/LabelerApp/editor/topicmodeller/documents/dynamicDictionaryEng.dict"
DynamicTopicsWordsStatisticsPathEng = "/home/forestg/projects/dipterv/LabelerApp/editor/topicmodeller/documents/dynamicTopicsWordsStatisticsPathEng.json"
DynamicTopicsPathEng = "/home/forestg/projects/dipterv/LabelerApp/editor/topicmodeller/documents/dynamicTopicsEng.json"


