# -*- coding: utf-8 -*-

import scrapy

from editor.langdetect.langdetectServices import langdetect


class IndexCrawler(scrapy.Spider):
    name = "index" # must be unique


    start_urls = [
        'http://index.hu',
    ]

    def parse(self, response):
        for href in response.css('a::attr(href)').re(r'.*dex.*'): # 1. kiszedjük a valid linkeket
            if not ("szerzo" in href) and not("mailto" in href) and ("id" in href): # 2. megszűrjük, csak a cikkekre mutatójk maradnak
                yield scrapy.Request(response.urljoin(href), callback=self.parse_article)
                # yield {
                #     'link': href,
                # }

    def parse_article(self, response):
        text = ''.join(response.css('div.cikk-torzs p::text').extract())
        yield{
            'url':response.url,
            'title':response.css('div.content-title h1 span::text').extract(),
            'text':text,
            'language':langdetect(text)
        }

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
