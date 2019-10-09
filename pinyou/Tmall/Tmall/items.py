# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TmallItem(scrapy.Item):
    # define the fields for your item here like:
    goodsid = scrapy.Field()
    word = scrapy.Field()
    pass

class Tmall_UIDItem(scrapy.Item):
    # define the fields for your item here like:
    goodsid = scrapy.Field()
    uid = scrapy.Field()
    pass

class TmallItemBrandname(scrapy.Item):
    # define the fields for your item here like:
    goodsid = scrapy.Field()
    brand_name = scrapy.Field()
    info = scrapy.Field()
    pass

class TaoBaoItem(scrapy.Item):
    itemId = scrapy.Field()
    goodsInfo = scrapy.Field()
