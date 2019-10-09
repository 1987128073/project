# -*- coding: utf-8 -*-
import datetime
import json
import logging
import re

import scrapy
from scrapy.utils.project import get_project_settings

from ..items import YunzkItem, DaTaoKeItem


class YzkSpider(scrapy.Spider):
    name = 'dataoke'
    allowed_domains = ['dataoke.com']

    def time_str(self, timeStamp):
        dateArray = datetime.datetime.utcfromtimestamp(timeStamp)
        otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
        return otherStyleTime

    def start_requests(self):
        for num in range(1, 825):
            yield scrapy.Request(url='http://www.dataoke.com/qlist/?page=%s' % num, callback=self.parse)

    def parse(self, response):
        settings = get_project_settings()
        item = DaTaoKeItem()
        r = response.xpath('/html/body/div[4]/div[3]/div[1]/div')
        for data in r:
            print(r.xpath('/div/div[2]/span/a/span[2]/text()').extract_first())
            # item['id'] = data.get('id')
            # item['name'] = data.get('name')
            item['auction_id'] = r.xpath('//@data_goodsid').extract_first()
            item['title'] = r[1].xpath('/div/div[2]/span/a/span[2]/text()').extract_first()
            item['intro'] = data.get('intro')
            item['pic'] = data.get('pic')
            item['sales_num'] = data.get('sales_num')
            item['is_tmall'] = data.get('is_tmall')
            item['seller_id'] = data.get('seller_id')
            item['cid'] = settings.get('GOODS_TYPE')[str(data.get('cid'))]
            item['coupon_id'] = data.get('coupon_id')
            item['coupon_price'] = data.get('coupon_price')
            item['coupon_end_time'] = self.time_str(data.get('coupon_end_time'))
            item['coupon_url'] = 'https://uland.taobao.com/coupon/edetail?activityId={}&itemId={}'.format(data.get('coupon_id'), data.get('auction_id'))
            item['add_time'] = self.time_str(data.get('add_time'))
            item['create_time'] = self.time_str(data.get('create_time'))
            yield item
