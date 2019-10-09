# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AnchoridspiderItem(scrapy.Item):
    # define the fields for your item here like:

    anchorId = scrapy.Field()
    anchorName = scrapy.Field()
    houseId = scrapy.Field()
    fansCount = scrapy.Field()
    liveCount = scrapy.Field()
    city = scrapy.Field()
    creatorType = scrapy.Field()
    darenScore = scrapy.Field()
    descText = scrapy.Field()
    anchorPhoto = scrapy.Field()
    organId = scrapy.Field()
    fansFeature = scrapy.Field()
    historyData = scrapy.Field()
    servType = scrapy.Field()
    pass

class AnchoridFansFeatureItem(scrapy.Item):

    anchorId = scrapy.Field()
    age = scrapy.Field()
    area = scrapy.Field()
    career = scrapy.Field()
    cate = scrapy.Field()
    gender = scrapy.Field()
    interest = scrapy.Field()

    pass

class OrganspiderItem(scrapy.Item):
    # define the fields for your item here like:

    organId = scrapy.Field()
    organText = scrapy.Field()
    organName = scrapy.Field()
    agencyPhoto = scrapy.Field()
    tag = scrapy.Field()
    catetgory = scrapy.Field()
    darenCount = scrapy.Field()
    topdrenCount = scrapy.Field()
    compositeScore = scrapy.Field()
    verticalField = scrapy.Field()
    platform = scrapy.Field()

    pass
