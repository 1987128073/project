# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Dp92Item(scrapy.Item):
    # define the fields for your item here like:
    Classification_one = scrapy.Field()
    Classification_two = scrapy.Field()
    Classification_three = scrapy.Field()
    title = scrapy.Field()
    Commentator = scrapy.Field()
    Commentator_lv = scrapy.Field()
    Comment = scrapy.Field()
    BrandName = scrapy.Field()
    CommodityName = scrapy.Field()
    video_url = scrapy.Field()
    Views_num = scrapy.Field()
    # comment_num = scrapy.Field()
    concerns_num = scrapy.Field()

    pass

