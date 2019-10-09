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

from ..items import AnchorspiderItem


class TbAnchorSpider(scrapy.Spider):
    name = 'tb_anchor'
    allowed_domains = ['zhiboshuju.com']

    def get_time(self):
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=7)
        n_days = now - delta
        data = n_days.strftime('%Y%m%d')
        return data

    def start_requests(self):
        settings = get_project_settings()
        r = redis.StrictRedis(host=settings.get('REDIS_IP'), port=settings.get('REDIS_PORT'), db=0, password=settings.get('REDIS_PASSWORD'))
        ID_LIST = r.smembers('anchorId')
        for i in ID_LIST:
            postdata = {
                'accountId': str(i.decode('utf-8')),
                'openId': 'ofYto04ZtE57zTesjffxdeWmZzQQ'
            }
            yield scrapy.FormRequest(
                url='https://www.zhiboshuju.com/analysis/selectaccount',
                method='post',
                formdata=postdata,
                dont_filter=True,
                callback=self.one_parse
            )

    def one_parse(self, response):
        json_obj = json.loads(response.text).get('data')
        if json_obj:
            anchorspiderItem = AnchorspiderItem()
            anchorspiderItem['accountId'] = json_obj.get('accountId')
            anchorspiderItem['accountName'] = json_obj.get('accountName')
            anchorspiderItem['fansNum'] = json_obj.get('fansNum')
            anchorspiderItem['headImg_url'] = json_obj.get('headImg')
            date = self.get_time()
            yield scrapy.FormRequest(
                                url='https://www.zhiboshuju.com/wxanchor/evetaobaoinfoself',
                                method='post',
                                headers={
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                                  'Chrome/75.0.3770.100 Safari/537.36',
                                    # 'Referer': 'https://www.zhiboshuju.com/shopWeChat/anchordata?openId=ofYto04ZtE57zTesjffxdeWmZzQQ&accountId={}&tapType=anchorTap'.format(anchorspiderItem['accountId']),
                                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
                                    },
                                formdata={
                                    'accountId': str(anchorspiderItem['accountId']),
                                    'openId': 'ofYto04ZtE57zTesjffxdeWmZzQQ',
                                    'date': date
                                },
                                meta={
                                    'anchorspiderItem': anchorspiderItem
                                },
                                dont_filter=True,
                                callback=self.two_parse
                            )

    def two_parse(self, response):
        meta = response.meta
        anchorspiderItem = meta.get('anchorspiderItem')
        json_obj = json.loads(response.text).get('data')
        if json_obj:
            anchorspiderItem['alliveId'] = json_obj.get('alliveId')
            anchorspiderItem['allpv'] = json_obj.get('allpv')
            anchorspiderItem['alluv'] = json_obj.get('alluv')
            anchorspiderItem['countitemId'] = json_obj.get('countitemId')
            anchorspiderItem['countshopId'] = json_obj.get('countshopId')
            anchorspiderItem['evepv'] = json_obj.get('evepv')
            anchorspiderItem['eveuv'] = json_obj.get('eveuv')
            anchorspiderItem['liveId'] = json_obj.get('liveId')
            date = self.get_time()

            yield scrapy.FormRequest(
                url='https://www.zhiboshuju.com/wxanchor/evetaobaoclass2scale',
                method='post',
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                  'Chrome/75.0.3770.100 Safari/537.36',
                    # 'Referer': 'https://www.zhiboshuju.com/shopWeChat/anchordata?openId=ofYto04ZtE57zTesjffxdeWmZzQQ&accountId={}&tapType=anchorTap'.format(anchorspiderItem['accountId']),
                    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
                },
                formdata={
                    'accountId': str(anchorspiderItem['accountId']),
                    'openId': 'ofYto04ZtE57zTesjffxdeWmZzQQ',
                    'date': date
                },
                meta={
                    'anchorspiderItem': anchorspiderItem
                },
                dont_filter=True,
                callback=self.parse
            )

    def parse(self, response):
        meta = response.meta
        anchorspiderItem = meta.get('anchorspiderItem')
        json_obj = json.loads(response.text).get('data')
        if json_obj:
            l = []
            for data in json_obj:
                item = {}
                item['class2Name'] = data.get('class2Name')
                item['class2Sid'] = data.get('class2Sid')
                item['classrate'] = data.get('classrate')
                item['date'] = data.get('date')
                l.append(item)
            anchorspiderItem['evetaobaoclass2scale'] = l
            yield anchorspiderItem