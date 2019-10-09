# -*- coding: utf-8 -*-
import json
import time
import redis
import scrapy
from scrapy.utils.project import get_project_settings

from ..items import TaoBaoItem as Item


class TmSpider(scrapy.Spider):
    name = 'tbGetGoodsInfoAPI'
    allowed_domains = ['taobao.com']
    settings = get_project_settings()

    def start_requests(self):

        r = redis.StrictRedis(host=self.settings.get('REDIS_IP'), port=self.settings.get('REDIS_PORT'),
                              password=self.settings.get('REDIS_PASSWORD'))
        while 1:
            itemId = r.spop('itemid')
            if not itemId:
                time.sleep(5)
            else:
                yield scrapy.Request(url='https://acs.m.taobao.com/gw/mtop.taobao.detail.getdetail/6.0/?data=%7B"itemNumId"%3A"{}"%7D'.format(itemId.decode('utf-8')), meta={'itemId': itemId.decode('utf-8')}, callback=self.parse)

    def parse(self, response):
        itemId = response.meta.get('itemId')
        data = json.loads(response.text).get('data')
        # print(data)
        item = Item()
        item['itemId'] = itemId
        item['goodsInfo'] = data

        # if data and data.get('item'):
        #     item = Item()
        #     item['itemId'] = data.get('item').get('itemId')
        #     item['goodsInfo'] = data.get('item')

        yield item
