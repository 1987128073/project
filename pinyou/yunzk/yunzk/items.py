# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YunzkItem(scrapy.Item):
    # define the fields for your item here like:
    # id = scrapy.Field()  # 商品id
    # name = scrapy.Field()  # 商品名称
    # seller_name = scrapy.Field()
    # shop_name = scrapy.Field()
    # update_time = scrapy.Field()
    # dtk = scrapy.Field()
    # ysd = scrapy.Field()
    # zhd = scrapy.Field()
    # hdk = scrapy.Field()
    auction_id = scrapy.Field()
    title = scrapy.Field()  # 商品标题
    d_title = scrapy.Field()  # 商店小标题
    intro = scrapy.Field()  # 卖点
    pic = scrapy.Field()  # 商品图片地址
    sales_num = scrapy.Field()  # 商品售量
    is_tmall = scrapy.Field()  # 商品是否在售
    seller_id = scrapy.Field()  # 商品的销售id
    cid = scrapy.Field()  # 商品类目id
    coupon_id = scrapy.Field()  # 商品优惠券id
    coupon_price = scrapy.Field()  # 优惠券价格
    coupon_end_time = scrapy.Field()  # 优惠券截至时间
    coupon_url = scrapy.Field()  # 优惠券地址：https://uland.taobao.com/coupon/edetail?activityId='coupon_id+'&itemId='auction_id
    add_time = scrapy.Field()  # 优惠券添加时间
    create_time = scrapy.Field()  # 优惠券添加时间
    pass

class DaTaoKeItem(scrapy.Item):
    # define the fields for your item here like:
    auction_id = scrapy.Field()  # 商品ID
    title = scrapy.Field()  # 商品标题
    intro = scrapy.Field()  # 卖点
    tmall_url = scrapy.Field()  # 商品天猫(淘宝)地址
    pic = scrapy.Field()  # 商品图片地址
    sales_num = scrapy.Field()  # 商品售量
    seller_id = scrapy.Field()  # 商品的销售id
    cid = scrapy.Field()  # 商品类目id
    coupon_price = scrapy.Field()  # 优惠券价格
    coupon_url = scrapy.Field()  # 优惠券地址
    # is_tmall = scrapy.Field()  # 商品是否在售
    # coupon_id = scrapy.Field()  # 商品优惠券id
    # d_title = scrapy.Field()  # 商店小标题
    # create_time = scrapy.Field()  # 优惠券添加时间
    # coupon_end_time = scrapy.Field()  # 优惠券截至时间
    # add_time = scrapy.Field()  # 优惠券添加时间
