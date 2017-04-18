# -*- coding: utf-8 -*-
import json
import os
from bs4 import BeautifulSoup

import scrapy
from langdetect import detect
from scrapy.selector import  Selector
from w3lib.html import remove_tags, remove_tags_with_content



class DynamicCrawler(scrapy.Spider):
    name = "dynamic" # must be unique
    counter = -1

    linkListPath = "/home/forestg/projects/dipterv/LabelerApp/data/linkLinst.json"

    if (os.path.exists(linkListPath)):
        with open(linkListPath) as data_file:
            links = json.load(data_file)
    else:
        raise ValueError(linkListPath+"<- this does not exists :(")

    start_urls = links

    def parse(self, response):
        sel = Selector(response)
        self.counter += 1

        # SZÖVEG TARTALOM KINYERÉSE
        # 1. összefűzzük a body tag tartalmát
        html = ''.join(response.css('body').extract())

        # 2. kiszedjük belőle a sortöréseket
        html_somewhat_striped = html.replace('\n','').strip()

        # 3. kitöröljük előle a felesleges tag-eket
        soup = BeautifulSoup(html_somewhat_striped)
        for script in soup(["script", "style"]):
            script.extract()    # rip it out
        text_ripped = soup.get_text()


        # 4. még egy adag formázás, biztos ami biztos
        lines = (line.strip() for line in text_ripped.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text_final = '\n'.join(chunk for chunk in chunks if chunk)

        # http://stackoverflow.com/questions/26603435/beautifulsoup-typeerror-nonetype-object-is-not-callable


        yield{
            'id': self.counter,
            'lang':detect(text_final),
            'url':response.url,
            'text':text_final,
        }
        # for href in response.css('a::attr(href)').re(r'.*dex.*'): # 1. kiszedjük a valid linkeket
        #     if not ("szerzo" in href) and not("mailto" in href) and not ("velvet" in href)and ("id" in href) \
    #     #             and not ("otthonterkep" in href) and not ("bookline" in href) and not ("totalcar" in href): # 2. megszűrjük, csak a cikkekre mutatójk maradnak
    #     #         yield scrapy.Request(response.urljoin(href), callback=self.parse_article)
    #     #         # yield {
    #     #         #     'link': href,
    #     #         # }.lc
    #
    # def parse_article(self, response):
    #     # author_meta_raw_list = response.css('meta').re(r'.*author.*')
    #
    #     # author_meta_raw = author_meta_raw_list[0] if author_meta_raw_list else None
    #
    #     # author_clean = ""
    #     # if(author_meta_raw):
    #     #     author_clean = BeautifulSoup(author_meta_raw)['content']
    #     # else:
    #     #     author_clean = "nincs"
    #     # # [u'<meta name="author" content="Munk Veronika">']
    #     # todo: írjár róla hogy az index válrtozrtatja a buzeráns oldalát
    #
    #     #Magyarázat: mindeközbenes blogfolyamnál egymás alá hányja a híreket, és nagyon elcseszi a dokumentumteret, ha mindig minden cikket behúzok...
    #     if("mindekozben" in response.url):
    #         textRaw = ''.join(response.css('div.clearafter').extract_first())
    #         from BeautifulSoup import BeautifulSoup
    #         text = BeautifulSoup(textRaw).text
    #     else:
    #         text = ''.join(response.css('div.cikk-torzs p::text').extract())
    #     self.counter += 1
    #
    #
    #     yield{
    #         'id': self.counter,
    #         'url':response.url,
    #         'title':response.css('div.content-title h1 span::text').extract_first(),
    #         'text':text,
    #     }

        # next_page = response.css('li.next a::attr(href)').extract_first()
        # if next_page is not None:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(next_page, callback=self.parse)












#https://docs.scrapy.org/en/latest/intro/tutorial.html

# scrapy shell "http://quotes.toscrape.com/page/1/"
# In [1]: response.css('title')
# Out[1]: [<Selector xpath=u'descendant-or-self::title' data=u'<title>Quotes to Scrape</title>'>]
#
# In [2]: response.css('title').extract()
# Out[2]: [u'<title>Quotes to Scrape</title>']
#
# In [3]: response.css('title::text').extract()
# Out[3]: [u'Quotes to Scrape']
#  quote = response.css("div.quote").extract_first()
#
