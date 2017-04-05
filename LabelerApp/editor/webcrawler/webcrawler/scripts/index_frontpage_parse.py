# -*- coding: utf-8 -*-
import os
import os.path

import sys


def parse_index_hu():
    # tester_path="data/quotes.json"
    tester_path="../data/index.json"
    print (sys.version)
    if(os.path.isfile(tester_path)):
        os.remove(tester_path)

    # os.system("scrapy crawl quotes -o data/quotes.json")
    os.system("scrapy crawl index -o ../data/index.json")


    # TODO FONTOS: a json fájlhoz hozzfáfűz a parancs! scrapy crawl quotes -o quotes.json
            # szóval megoldás, ezt töröltetni kell sajnos.

# parse_index_hu()
