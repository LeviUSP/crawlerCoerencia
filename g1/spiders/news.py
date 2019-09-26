# -*- coding: utf-8 -*-
import scrapy
from g1.items import G1Item
import codecs

class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['g1.globo.com']
    start_urls = ['http://g1.globo.com/']


    def parse(self, response):

        for article in response.css("div.feed-post-body"):
            link = article.css("a ::attr(href)").extract_first()

            yield response.follow(link, self.parse_article)


        next_page = response.css("div.load-more.gui-color-primary-bg a::attr(href)").extract()
        
        if next_page is not None:
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        link = response.url 
        title = response.css("h1.content-head__title ::text").extract_first()
        author = response.css("p.content-publication-data__from  ::text").extract_first()
        text = "".join(response.css("p.content-text__container ::text").extract())

        
        output_string = title.encode('utf-8')

        with codecs.open(output_string +'.txt','w', 'utf-16') as f:
            f.seek(0)
            f.write(text)

        notice = G1Item(title=title, author=author, text=text, link=link)
        yield notice