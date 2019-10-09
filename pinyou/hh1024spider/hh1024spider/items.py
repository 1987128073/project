# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class hh1024LivelistAPI(scrapy.Item):
    # define the fields for your item here like:
    itemId = scrapy.Field()
    itemUrl = scrapy.Field()
    pictUrl = scrapy.Field()
    reservePrice = scrapy.Field()
    title = scrapy.Field()
    pass

class hh1024AnchorAPIItem(scrapy.Item):
    # define the fields for your item here like:
    anchorId = scrapy.Field()
    With_cargo_goods = scrapy.Field()
    pass
