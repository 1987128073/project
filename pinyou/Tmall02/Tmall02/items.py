# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class Tmall02Item(scrapy.Item):
    # define the fields for your item here like:
    shopid = scrapy.Field()
    pass

class TmallItem(scrapy.Item):
    # define the fields for your item here like:
    goodsid = scrapy.Field()
    keyword = scrapy.Field()
    pass

class couponItem(scrapy.Item):
    category = Field()
    commission_rate = Field()
    coupon_click_url = Field()
    coupon_end_time = Field()
    coupon_info = Field()
    coupon_remain_count = Field()
    coupon_start_time = Field()
    coupon_total_count = Field()
    item_description = Field()
    item_url = Field()
    nick = Field()
    num_iid = Field()
    pict_url = Field()
    seller_id = Field()
    shop_title = Field()
    title = Field()
    user_type = Field()
    volume = Field()
    zk_final_price = Field()
