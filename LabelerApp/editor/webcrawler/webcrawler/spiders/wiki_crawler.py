import scrapy
from BeautifulSoup import BeautifulSoup

class WikiCrawper(scrapy.Spider):
    name = "wiki"
    counter = 0

    start_urls = [
        'https://hu.wikipedia.org/wiki/Kezd%C5%91lap'
    ]

    def parse(self, response):
        for href in response.css('a::attr(href)').re(r'.*wiki.*'):
            yield scrapy.Request(response.urljoin(href), callback=self.parse_article)

    def parse_article(self, response):
        text_with_html_tags = response.css('div.mw-content-ltr p').extract_first()
        cleantext = BeautifulSoup(text_with_html_tags).text
        self.counter += 1

        yield{
            'id' : self.counter,
            'lang':langdetect(cleantext),
            'url':response.url,
            'title':response.css('title::text').extract_first(),
            'text':cleantext,
        }

from langdetect import detect, detect_langs


def langdetect(text):
    return detect(text)
