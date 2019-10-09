# -*- coding: utf-8 -*-
import datetime
import json
import logging
import os
import time
import redis
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.utils.project import get_project_settings
from ..items import AnchorspiderItem, AnchorShopspiderItem


class TbAnchorSpider(scrapy.Spider):
    name = 'tb_anchor_goods'
    allowed_domains = ['zhiboshuju.com']


    def get_time(self):
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=7)
        n_days = now - delta
        data = n_days.strftime('%Y%m%d')
        return data

    def get_redis_data(self):
        settings = get_project_settings()
        r = redis.StrictRedis(host=settings.get('REDIS_IP'), port=settings.get('REDIS_PORT'), db=0,
                              password=settings.get('REDIS_PASSWORD'))
        ID_LIST = r.smembers('anchorId')
        return ID_LIST

    def start_requests(self):
        settings = get_project_settings()
        r = redis.StrictRedis(host=settings.get('REDIS_IP'), port=settings.get('REDIS_PORT'), db=0,
                              password=settings.get('REDIS_PASSWORD'))

        while 1:
            anchorid = r.spop('need_update_anchor_Id')
            if anchorid:
                postdata = {
                    'accountId': str(anchorid.decode('utf-8')),
                    'openId': 'ofYto04ZtE57zTesjffxdeWmZzQQ',
                    'page': '1',
                    'limit': '1000',
                    'rootCategoryId': ''
                }
                yield scrapy.FormRequest(
                    url='https://www.zhiboshuju.com/shopanchorWeChat/selectaccountsevendate',
                    method='post',
                    formdata=postdata,
                    dont_filter=True,
                    callback=self.parse
                )
            else:
                time.sleep(5)


    def parse(self, response):

        anchorspiderItem = AnchorShopspiderItem()
        json_obj = json.loads(response.text).get('data')
        if json_obj:
            for data in json_obj:
                anchorspiderItem['accountId'] = data['accountId']  # 主播ID
                anchorspiderItem['accountName'] = data['accountName']  # 主播昵称
                anchorspiderItem['title'] = data['title']  # 商品标题
                anchorspiderItem['createTime'] = data['createTime']  # 商品上架时间
                anchorspiderItem['itemId'] = data['itemId']  # 商品ID
                anchorspiderItem['sellerId'] = data['sellerId']  # 商品售卖ID
                anchorspiderItem['goods_url'] = 'https://detail.tmall.com/item.htm?id=' + data['itemId']
                anchorspiderItem['shopName'] = data['shopName']  # 商店名称
                anchorspiderItem['liveId'] = data['liveId']  # 直播间ID
                anchorspiderItem['liveURL'] = 'http://huodong.m.taobao.com/act/talent/live.html?id=%s' % data['liveId']  # 直播间URL
                anchorspiderItem['livePrice'] = data['livePrice']  # 商品直播时的价格
                anchorspiderItem['categoryId'] = data['categoryId']  # 商品分类ID
                anchorspiderItem['class2name'] = data['class2name']  # 商品所属类别
                anchorspiderItem['shopId'] = data['shopId']  # 商店ID
                anchorspiderItem['shopType'] = data['shopType']  # 商店级别
                anchorspiderItem['maintype'] = data['maintype']  # 商品主分类
                anchorspiderItem['rootCategoryId'] = data['rootCategoryId']
                yield anchorspiderItem