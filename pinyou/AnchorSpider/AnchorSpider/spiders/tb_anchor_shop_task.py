# -*- coding: utf-8 -*-
import json
import time
import redis
import scrapy
from scrapy.utils.project import get_project_settings
from ..items import AnchorShopspiderItem


class AnchorInfoSpider(scrapy.Spider):
    name = 'tb_anchor_goods_task'  # 任务发布到redis中的anchorId_task中
    # allowed_domains = ['zhiboshuju.com']
    settings = get_project_settings()
    r = redis.StrictRedis(host=settings.get('REDIS_IP'), port=settings.get('REDIS_PORT'), db=0,
                          password=settings.get('REDIS_PASSWORD'))

    def start_requests(self):

        while 1:
            anchorid = self.r.spop('anchorId:anchorName')
            if anchorid:
                postdata = {
                    'accountId': str(anchorid.decode('utf-8').split(':')[0]),
                    'openId': 'ofYto04ZtE57zTesjffxdeWmZzQQ',
                    'page': '1',
                    'limit': '1000',
                    'rootCategoryId': ''
                }

                yield scrapy.FormRequest(
                    url='https://www.zhiboshuju.com/shopanchorWeChat/selectaccountsevendate',
                    method='POST',
                    formdata=postdata,
                    dont_filter=True,
                    # meta={'anchorId': str(anchorid.decode('utf-8').split(':')[0])},
                    callback=self.parse,

                )
            else:
                time.sleep(5)

    def parse(self, response):
        anchorId = response.meta.get('anchorId')
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
                anchorspiderItem['rootCategoryId'] = data['rootCategoryId']  #
                yield anchorspiderItem
            self.r.sadd('finish_anchorId', "{}:{}".format(anchorId, 1))
        else:
            self.r.sadd('finish_anchorId', "{}:{}".format(anchorId, 0))
