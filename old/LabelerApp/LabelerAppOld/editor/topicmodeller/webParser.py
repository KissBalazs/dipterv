# -*- coding: utf-8 -*-
__author__ = 'forestg'

from bs4 import BeautifulSoup
import requests



def parse_content(soup):
    l = soup.findAll('p')
    return " ".join(map(lambda x: x.text, l))

def getWebContent(urlText):
    #soup = BeautifulSoup(urlText)
    # returnText = parse_content(soup)
    resp = requests.get(urlText)
    soup = BeautifulSoup(resp.text)
    returnText = (parse_content(soup))
    return returnText

def getPostLabels(urlText):
    resp = requests.get(urlText)
    soup = BeautifulSoup(resp.text)
    l = soup.findAll('meta', {'property':'article:tag'})
    tags = []
    for v in l:
        tags.append(v['content'])
    return tags

def getLinks(text):
    returnText = text.split()
    return returnText

def parse_title(urlText):
    resp = requests.get(urlText)
    soup = BeautifulSoup(resp.text)
    return soup.find('h1').text


# # Példa kód innentől lefelé:
# def parse_labels(soup):
#     l = soup.findAll('meta', {'property':'article:tag'})
#     tags = []
#     for v in l:
#         tags.append(v['content'])
#     return tags
#
# def parse_title(soup):
#     return soup.find('h1').text
#
# def parse_lead(soup):
#     return soup.find('div', {'class':'articleLead'}).text.strip()
#
# def parse_meta(soup):
#     pubtime = soup.find('meta', {'property':'article:published_time'})['content']
#     modtime = soup.find('meta', {'property':'article:modified_time'})['content']
#     section = soup.find('meta', {'property':'article:section'})['content']
#     return pubtime, modtime, section
#
#
# for url in urllist:
#     print (url)
#     resp = requests.get(url)
#     soup = BeautifulSoup(resp.text)
#     print (parse_labels(soup))
#     print (parse_content(soup))
#     print ("----")
# # ------------------ itt ér véget a példa kód
