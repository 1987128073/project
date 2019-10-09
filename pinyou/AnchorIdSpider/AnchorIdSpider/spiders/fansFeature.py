# -*- coding: utf-8 -*-
import datetime
import logging
import json
import redis
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.utils.project import get_project_settings
from ..items import AnchoridFansFeatureItem as AnchorItem


class TbAnchorSpider(scrapy.Spider):
    name = 'fansFeature'
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

    def getAnchorId(self, key):

        r = redis.StrictRedis(host=self.settings.get('REDIS_IP'), port=self.settings.get('REDIS_PORT'), db=0, password=self.settings.get('REDIS_PASSWORD'))
        return r.smembers(key)

    def start_requests(self):
        num = 0
        for id in self.getAnchorId('accountId'):
            num = num + 1
            yield scrapy.Request(
                url='https://v.taobao.com/micromission/daren/qry_fans_portrait.do?userId={}'.format(id.decode('utf-8')),
                headers=self.headers,
                callback=self.parse,
                meta={
                    'anchorId': id.decode('utf-8'),
                    'num': num
                      }
            )

    def parse(self, response):
        accountId = response.meta.get('anchorId')
        anchorItem = AnchorItem()
        json_obj = json.loads(response.text).get('data')

        if json.loads(response.text).get('msg') != '成功':
            logging.error('获取数据失败：{}: {}'.format(response.meta.get('num'), accountId))
            self.failToGet(accountId)

        if json_obj and json_obj.get('fansFeature'):
            json_obj = json_obj.get('fansFeature')
            anchorItem['anchorId'] = accountId
            anchorItem['age'] = json_obj.get('age')
            anchorItem['area'] = json_obj['area']
            anchorItem['career'] = json_obj['career']
            anchorItem['cate'] = json_obj['cate']
            anchorItem['gender'] = json_obj['gender']
            anchorItem['interest'] = json_obj['interest']
            yield anchorItem
        else:
            anchorItem['anchorId'] = accountId
            anchorItem['age'] = None
            anchorItem['area'] = None
            anchorItem['career'] = None
            anchorItem['cate'] = None
            anchorItem['gender'] = None
            anchorItem['interest'] = None
            yield anchorItem

