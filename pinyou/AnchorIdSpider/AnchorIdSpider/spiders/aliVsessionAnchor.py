# -*- coding: utf-8 -*-
import datetime
import json
import redis
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.utils.project import get_project_settings
from ..items import AnchoridspiderItem as AnchorItem


class TbAnchorSpider(scrapy.Spider):
    name = 'aliVsessionAnchor'
    allowed_domains = ['taobao.com']
    settings = get_project_settings()
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'cookie': settings.get('COOKIE'),
        'referer': 'https://v.taobao.com/v/content/live?spm=a21xh.11312869.fastEntry.8.75a8627fl7u5OW&catetype=701',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }

    def failToGet(self, accountId):

        r = redis.StrictRedis(host=self.settings.get('REDIS_IP'), port=self.settings.get('REDIS_PORT'), db=0, password=self.settings.get('REDIS_PASSWORD'))
        r.sadd('FailToGetAccountId', accountId)

    def start_requests(self):
        for page in range(1, 251):
            yield scrapy.Request(
                url='https://v.taobao.com/micromission/req/selectCreatorV3.do?cateType=701&currentPage={}&_output_charset=UTF-8&_input_charset=UTF-8'.format(page),
                headers=self.headers,
                callback=self.one_parse
            )

    def one_parse(self, response):
        json_obj = json.loads(response.text).get('data')
        if json_obj and json_obj.get('result'):
            for data in json_obj.get('result'):
                id = data.get('userId')
                servType = data.get('servType')
                yield scrapy.Request(
                                    url='https://v.taobao.com/micromission/daren/daren_main_portalv3.do?userId={}&spm=a21xh.11312873.701.1.58887001iWrzZu'.format(id),
                                    headers=self.headers,
                                    callback=self.parse,
                                    meta={'anchorId': id, 'servType': servType}
                                )

    def parse(self, response):
        accountId = response.meta.get('anchorId')
        servType = response.meta.get('servType')
        anchorItem = AnchorItem()
        json_obj = json.loads(response.text).get('data')

        if json.loads(response.text).get('msg') != '成功':
            self.failToGet(accountId)

        if json_obj:
            anchorItem['anchorId'] = accountId
            anchorItem['fansCount'] = json_obj.get('fansCount')
            anchorItem['anchorName'] = json_obj['darenNick']
            try:
                anchorItem['city'] = json_obj['city']
            except:
                anchorItem['city'] = None

            try:
                anchorItem['creatorType'] = json_obj['creatorType']
            except:
                anchorItem['creatorType'] = None

            anchorItem['darenScore'] = json_obj['darenScore']
            anchorItem['descText'] = json_obj['desc']  # 此字段为一段json数据
            anchorItem['anchorPhoto'] = 'https:' + json_obj['picUrl']
            try:
                anchorItem['organId'] = json_obj.get('darenAgency').get('agencyID')
            except:
                anchorItem['organId'] = None  # 次主播未与别的机构合作
            anchorItem['servType'] = servType
            yield anchorItem
