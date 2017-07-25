# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScarpyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    rank = scrapy.Field()
    keyword = scrapy.Field()
    platformId = scrapy.Field()
    userId = scrapy.Field()
    webId = scrapy.Field()
    keywordId = scrapy.Field()
    priceone = scrapy.Field()
    pricetwo = scrapy.Field()