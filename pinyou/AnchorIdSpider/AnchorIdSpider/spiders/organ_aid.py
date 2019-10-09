# -*- coding: utf-8 -*-
import csv
import datetime
import json
import logging
import os
import redis
import requests
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.utils.project import get_project_settings
from ..items import OrganspiderItem as AnchorItem


class TbAnchorSpider(scrapy.Spider):
    name = 'organ_info'
    allowed_domains = ['taobao.com']
    settings = get_project_settings()
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'cookie': settings.get('COOKIE'),
        'referer': 'https://v.taobao.com/v/content/live?spm=a21xh.11312869.fastEntry.8.75a8627fl7u5OW&catetype=702',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }

    def failToGet(self, OrganId):

        r = redis.StrictRedis(host=self.settings.get('REDIS_IP'), port=self.settings.get('REDIS_PORT'), db=0,
                              password=self.settings.get('REDIS_PASSWORD'))
        r.sadd('FailToGeOrganId', OrganId)

    def get_totalCounts(self):  # 拿到总页码
        json_obj = requests.get(
            url='https://v.taobao.com/micromission/req/selectCreatorV3.do?_output_charset=UTF-8&cateType=702&currentPage=1&_input_charset=UTF-8',
            headers=self.headers).json()
        if json_obj and json_obj.get('data'):
            return json_obj.get('data').get('totalCounts')
        else:
            return None

    def start_requests(self):
        if self.get_totalCounts():
            for page in range(1, int(self.get_totalCounts())//20+2):
                yield scrapy.Request(
                    url='https://v.taobao.com/micromission/req/selectCreatorV3.do?_output_charset=UTF-8&cateType=702&currentPage={}&_input_charset=UTF-8'.format(page),
                    headers=self.headers,
                    callback=self.one_parse
                )

    def one_parse(self, response):
        json_obj = json.loads(response.text).get('data')
        if json_obj and json_obj.get('result'):
            for data in json_obj.get('result'):
                organ_id = data.get('userId')
                tag = data.get('tag')
                yield scrapy.Request(
                                    url='https://v.taobao.com/micromission/daren/daren_main_portalv3.do?userId={}'.format(organ_id),
                                    headers=self.headers,
                                    callback=self.parse,
                                    meta={
                                        'organ_Id': organ_id,
                                        'tag': tag,
                                    }
                                )

    def parse(self, response):
        organ_id = response.meta.get('organ_Id')
        tag = response.meta.get('tag')
        OrganspiderItem = AnchorItem()
        json_obj = json.loads(response.text).get('data')

        if json.loads(response.text).get('msg') != '成功':
            self.failToGet(organ_id)

        if json_obj:
            OrganspiderItem['organId'] = organ_id
            OrganspiderItem['organText'] = json_obj.get('introSummary')
            OrganspiderItem['organName'] = json_obj.get('darenNick')
            OrganspiderItem['agencyPhoto'] = json_obj.get('picUrl')
            OrganspiderItem['tag'] = tag
            try:
                OrganspiderItem['catetgory'] = json_obj.get('darenMissionData').get('servType')
            except:
                OrganspiderItem['catetgory'] = None
            OrganspiderItem['darenCount'] = json_obj.get('darenCount')
            try:
                OrganspiderItem['topdrenCount'] = len(json_obj.get('bigShots'))
            except:
                OrganspiderItem['topdrenCount'] = None
            OrganspiderItem['compositeScore'] = json_obj.get('darenScore')
            OrganspiderItem['verticalField'] = json_obj.get('area')

            yield OrganspiderItem

