# -*- coding: utf-8 -*-
import os
import os.path

import sys

from editor.topicmodeller.utils.consts import IndexDocumentsPath


def parse_index_hu():
    import subprocess

    # tester_path="data/quotes.json"
    tester_path= IndexDocumentsPath
    print (sys.version)
    if(os.path.isfile(tester_path)):
        os.remove(tester_path)

    os.system("cd /home/forestg/projects/dipterv/LabelerApp/editor/webcrawler; scrapy crawl index -o "+ IndexDocumentsPath)


    # TODO FONTOS: a json fájlhoz hozzfáfűz a parancs! scrapy crawl quotes -o quotes.json
            # szóval megoldás, ezt töröltetni kell sajnos.

# parse_index_hu()
