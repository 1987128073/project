# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DarenjispiderItem(scrapy.Item):
    # define the fields for your item here like:
    anchorName = scrapy.Field()
    roomNumber = scrapy.Field()
    category = scrapy.Field()
    liveCount = scrapy.Field()
    pass
