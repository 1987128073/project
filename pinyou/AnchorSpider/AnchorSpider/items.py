# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AnchorspiderItem(scrapy.Item):
    accountId = scrapy.Field()
    accountName = scrapy.Field()
    fansNum = scrapy.Field()
    headImg_url = scrapy.Field()
    alliveId = scrapy.Field()
    allpv = scrapy.Field()
    alluv = scrapy.Field()
    countitemId = scrapy.Field()
    countshopId = scrapy.Field()
    evepv = scrapy.Field()
    eveuv = scrapy.Field()
    liveId = scrapy.Field()
    evetaobaoclass2scale = scrapy.Field()
    pass

class DevAnchorspiderItem(scrapy.Item):
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


    pass

class AnchorShopspiderItem(scrapy.Item):
    accountId = scrapy.Field()
    accountName = scrapy.Field()
    title = scrapy.Field()
    itemId = scrapy.Field()
    sellerId = scrapy.Field()
    goods_url = scrapy.Field()
    shopName = scrapy.Field()
    liveId = scrapy.Field()
    liveURL = scrapy.Field()
    livePrice = scrapy.Field()
    categoryId = scrapy.Field()
    class2name = scrapy.Field()
    shopId = scrapy.Field()
    shopType = scrapy.Field()
    maintype = scrapy.Field()
    rootCategoryId = scrapy.Field()
    createTime = scrapy.Field()

    pass

class AnchorIdspiderItem(scrapy.Item):

    anchorId = scrapy.Field()
    anchorName = scrapy.Field()
    anchorPicture = scrapy.Field()
    endLiveTime = scrapy.Field()
    goodsIndex = scrapy.Field()
    itemId = scrapy.Field()
    startLiveTime = scrapy.Field()
    topic = scrapy.Field()

    pass


class TaoBaoItem(scrapy.Item):
    sellcount = scrapy.Field()

    pass