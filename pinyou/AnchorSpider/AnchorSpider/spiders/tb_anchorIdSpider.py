# -*- coding: utf-8 -*-
import csv
import datetime
import json
import logging
import os

import redis
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.utils.project import get_project_settings

from ..items import AnchorspiderItem, AnchorIdspiderItem


class TbAnchorSpider(scrapy.Spider):
    name = 'tb_anchorid'
    allowed_domains = ['zhiboshuju.com']

    def time_str(self, timeStamp):
        if timeStamp:
            dateArray = datetime.datetime.utcfromtimestamp(timeStamp/1000 + 8*60*60)
            otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
        else:
            otherStyleTime = None
        return otherStyleTime

    def start_requests(self):
        settings = get_project_settings()
        # r = redis.StrictRedis(host=settings.get('REDIS_IP'), port=settings.get('REDIS_PORT'), db=0, password=settings.get('REDIS_PASSWORD'))
        # ID_LIST = r.smembers('AnchorID')
        for i in range(1, 140):
            postdata = {
                'pageIndex': str(i),
            }
            yield scrapy.FormRequest(
                url='https://www.zhiboshuju.com/common/itemSpecialpush',
                method='post',
                formdata=postdata,
                # dont_filter=True,
                callback=self.one_parse
            )

    def one_parse(self, response):
        json_obj = json.loads(response.text).get('data')
        if json_obj and json_obj.get('response') and json_obj.get('response').get('body'):

            for data in json_obj.get('response').get('body'):

                yield scrapy.FormRequest(
                                    url='https://www.zhiboshuju.com/product/getAnchorProductInfo',
                                    method='post',
                                    headers={
                                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                                      'Chrome/75.0.3770.100 Safari/537.36',
                                        # 'Referer': 'https://www.zhiboshuju.com/shopWeChat/anchordata?openId=ofYto04ZtE57zTesjffxdeWmZzQQ&accountId={}&tapType=anchorTap'.format(anchorspiderItem['accountId']),
                                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                                        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
                                        },
                                    formdata={
                                        'itemId': str(data.get('itemId'))
                                    },
                                    # dont_filter=True,
                                    callback=self.parse
                                )

    def parse(self, response):
        anchorIdspiderItem = AnchorIdspiderItem()
        json_obj = json.loads(response.text).get('data')
        if json_obj:
            for data1 in json_obj:

                anchorIdspiderItem['itemId'] = data1.get('itemId')
                anchorIdspiderItem['anchorId'] = data1['anchorId']
                anchorIdspiderItem['anchorName'] = data1['anchorName']
                anchorIdspiderItem['anchorPicture'] = data1['anchorPicture']
                anchorIdspiderItem['endLiveTime'] = self.time_str(data1['endLiveTime'])
                anchorIdspiderItem['goodsIndex'] = data1['goodsIndex']
                anchorIdspiderItem['startLiveTime'] = self.time_str(data1['startLiveTime'])
                anchorIdspiderItem['topic'] = data1['topic']
                yield anchorIdspiderItem

