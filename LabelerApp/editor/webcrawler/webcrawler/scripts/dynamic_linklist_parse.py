# -*- coding: utf-8 -*-
import json
import os
import os.path

import sys

from editor.topicmodeller.utils.consts import IndexDocumentsPath, linkListDocumentsPath


def parse_dynamic_linklist():
    if(os.path.isfile(linkListDocumentsPath)):
        os.remove(linkListDocumentsPath)



    os.system("cd /home/forestg/projects/dipterv/LabelerApp/editor/webcrawler; scrapy crawl dynamic -o "+ linkListDocumentsPath)
