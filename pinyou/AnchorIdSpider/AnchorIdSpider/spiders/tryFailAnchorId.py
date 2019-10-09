# -*- coding: utf-8 -*-
import datetime
import json
import redis
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.utils.project import get_project_settings
from ..items import AnchoridspiderItem as AnchorItem


class TbAnchorSpider(scrapy.Spider):
    name = 'tryFailAnchorId'
    allowed_domains = ['taobao.com']
    settings = get_project_settings()
    headers = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'cookie': settings.get('COOKIE'),
        'referer': 'https://v.taobao.com/v/content/live?spm=a21xh.11312869.fastEntry.8.75a8627fl7u5OW&catetype=701',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
    }

    def failToGet(self, accountId):
        settings = get_project_settings()
        r = redis.StrictRedis(host=settings.get('REDIS_IP'), port=settings.get('REDIS_PORT'), db=0, password=settings.get('REDIS_PASSWORD'))
        r.sadd('FailToGetAccountId', accountId)

    def start_requests(self):
        settings = get_project_settings()
        r = redis.StrictRedis(host=settings.get('REDIS_IP'), port=settings.get('REDIS_PORT'), db=0,
                              password=settings.get('REDIS_PASSWORD'))
        while 1:
            id = r.spop('FailToGetAccountId')
            if id:
                yield scrapy.Request(
                    url='https://v.taobao.com/micromission/daren/daren_main_portalv3.do?userId={}&spm=a21xh.11312873.701.1.58887001iWrzZu'.format(id.decode('utf-8')),
                    headers=self.headers,
                    callback=self.parse,
                    meta={'anchorId': id.decode('utf-8')}
                )
            else:
                break

    def parse(self, response):
        accountId = response.meta.get('anchorId')
        # servType = response.meta.get('servType')
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
            anchorItem['creatorType'] = json_obj['creatorType']
            anchorItem['darenScore'] = json_obj['darenScore']
            anchorItem['descText'] = json_obj['desc']  # 此字段为一段json数据
            anchorItem['anchorPhoto'] =  'https:' + json_obj['picUrl']
            try:
                anchorItem['organId'] = json_obj.get('darenAgency').get('agencyID')
            except:
                anchorItem['organId'] = None  # 次主播未与别的机构合作
            try:
                anchorItem['servType'] = json_obj['area']
            except:
                anchorItem['servType'] = None
            yield anchorItem

