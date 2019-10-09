# -*- coding: utf-8 -*-
import datetime
import json
import logging
import re

import scrapy
from scrapy.utils.project import get_project_settings

from ..items import YunzkItem


class YzkSpider(scrapy.Spider):
    name = 'yzk'
    allowed_domains = ['iyunzk.com']

    def time_str(self, timeStamp):
        dateArray = datetime.datetime.utcfromtimestamp(int(timeStamp))
        otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
        return otherStyleTime


    def start_requests(self):
        for num in range(1, 2244):
            yield scrapy.Request(url='http://ku.iyunzk.com/?p=%s' % num, callback=self.parse)

    def parse(self, response):
        settings = get_project_settings()
        item = YunzkItem()
        pattern = re.compile(r'itemData: ([\s\S].*)cateData: {', re.S)
        a = re.search(pattern, response.text).group(1)[:-6]
        r = json.loads(a)
        for data in r:
            # item['id'] = data.get('id')
            # item['name'] = data.get('name')
            item['auction_id'] = data.get('auction_id')
            item['title'] = data.get('title')
            item['d_title'] = data.get('d_title')
            item['intro'] = data.get('intro')
            item['pic'] = data.get('pic')
            item['sales_num'] = data.get('sales_num')
            item['is_tmall'] = data.get('is_tmall')
            item['seller_id'] = data.get('seller_id')
            item['cid'] = settings.get('GOODS_TYPE')[str(data.get('cid'))]
            item['coupon_id'] = data.get('coupon_id')
            item['coupon_price'] = data.get('coupon_price')
            item['coupon_end_time'] = self.time_str(data.get('coupon_end_time'))
            item['coupon_url'] = 'https://uland.taobao.com/coupon/edetail?activityId={}&itemId={}'.format(
                data.get('coupon_id'), data.get('auction_id'))
            item['add_time'] = self.time_str(data.get('add_time'))
            item['create_time'] = self.time_str(data.get('create_time'))
            yield item
