# -*- coding: utf-8 -*-
import os
import os.path

import sys


def parse_wiki_hu():
    import subprocess

    # tester_path="data/quotes.json"
    tester_path="/home/forestg/projects/dipterv/LabelerApp/data/wiki.json"
    print (sys.version)
    if(os.path.isfile(tester_path)):
        os.remove(tester_path)

    # os.system("scrapy crawl wiki -o ../data/wiki.json")
    os.system("cd /home/forestg/projects/dipterv/LabelerApp/editor/webcrawler; scrapy crawl wiki -o /home/forestg/projects/dipterv/LabelerApp/data/wiki.json")



# todo: futtatáshoz kommentezd ezt ki
# parse_wiki_hu()
