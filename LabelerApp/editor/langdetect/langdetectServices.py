# -*- coding: utf-8 -*-
__author__ = 'forestg'

from langdetect import detect, detect_langs


def langdetect(text):
    # print(detect_langs(text)) megadja a teljes mátrixot, de külün futás, nem determinisztikus!
    return detect(text)
#
#
# print(langdetect(u"I have a nice car"))
# print(langdetect(u"Ich bin Balázs"))
# print(langdetect(u"Sziasztok kedves vendégeim üdvözüljük önöket itthon"))

#  todo: erről írj a dogába http://stackoverflow.com/questions/21129020/how-to-fix-unicodedecodeerror-ascii-codec-cant-decode-byte
# mystring1 = u"Ich bin Balázs, Ein, zwei, drei"
# mystring2 = "Ich bin Balázs, Ein, zwei, drei"
# print(type(mystring1))
# print(type(mystring2))
