# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class productItem(scrapy.Item):
    product_id = scrapy.Field()
    product_name = scrapy.Field()
    product_sales = scrapy.Field()
    product_shop_name = scrapy.Field()
    product_price = scrapy.Field()
    product_shop_type = scrapy.Field()
    product_shop_ww = scrapy.Field()
    product_shop_id = scrapy.Field()

class anchorItem(scrapy.Item):
    anchor_id = scrapy.Field()
    anchor_name = scrapy.Field()
    shop_id = scrapy.Field()

class shopItem(scrapy.Item):
    shop_id = scrapy.Field()
    shop_ww = scrapy.Field()
    shop_name = scrapy.Field()
    shop_sales = scrapy.Field()
    shop_type = scrapy.Field()
    shop_grade = scrapy.Field()
    main_class = scrapy.Field()
    shop_mas = scrapy.Field()  # 描述相符
    shop_sas = scrapy.Field()  # 服务态度速度
    shop_cas = scrapy.Field()  # 发货速度
    anchor_num = scrapy.Field()

class GoodsdataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
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

