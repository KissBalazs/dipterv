# -*- coding: utf-8 -*-

import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes" # must be unique

    # def start_requests(self):  # iterálható Request, innen indul a "mászás"
    #     urls = [
    #         'http://quotes.toscrape.com/page/1/',
    #         'http://quotes.toscrape.com/page/2/',
    #     ]
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)
    # def parse(self, response): # callback, ha letöltötte a lekérést
    #     page = response.url.split("/")[-2]
    #     filename = 'quotes-%s.html' % page
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)
    #     self.log('Saved file %s' % filename)

    # start_urls = [ # ez egyszeűbb módja shortcut a start_request helyett (van defaul implementáció)
    #     'http://quotes.toscrape.com/page/1/',
    #     'http://quotes.toscrape.com/page/2/',
    # ]
    # def parse(self, response):
    #     for quote in response.css('div.quote'):
    #         yield {
    #             'text': quote.css('span.text::text').extract_first(),
    #             'author': quote.css('small.author::text').extract_first(),
    #             'tags': quote.css('div.tags a.tag::text').extract(),
    #         }

    start_urls = [
        'http://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('small.author::text').extract_first(),
                'tags': quote.css('div.tags a.tag::text').extract(),
            }

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    # TODO FONTOS: a json fájlhoz hozzfáfűz a parancs! scrapy crawl quotes -o quotes.json
            # szóval megoldás, ezt töröltetni kell sajnos.










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
