# -*- coding: utf-8 -*-
import datetime
import json
import redis
import requests
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.utils.project import get_project_settings
from ..items import AnchoridspiderItem as AnchorItem


class TbAnchorSpider(scrapy.Spider):
    name = 'searchAnchorAPI'
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

    def getTotalCounts(self, name):
        json_obj = requests.get(url='https://v.taobao.com/micromission/req/selectCreatorV3.do?cateType=701&nick={}&currentPage=1&_output_charset=UTF-8&_input_charset=UTF-8'.format(name), headers=self.headers).json()
        data = json_obj.get('data')
        if data:
            try:
                count = int(data.get('totalCounts'))
            except:
                count = 19
            return count
        else:
            return 19


    def start_requests(self):
        r = redis.StrictRedis(host=self.settings.get('REDIS_IP'), port=self.settings.get('REDIS_PORT'), db=0,
                              password=self.settings.get('REDIS_PASSWORD'))
        while 1:
            name = r.spop('name')
            if name:
                totalcounts = self.getTotalCounts(name.decode('utf-8'))
                if totalcounts // 20 == 0:
                    num = 1
                else:
                    num = totalcounts // 20 + 1
                for page in range(num):
                    yield scrapy.Request(
                        url='https://v.taobao.com/micromission/req/selectCreatorV3.do?cateType=701&nick={}&currentPage={}&_output_charset=UTF-8&_input_charset=UTF-8'.format(
                            name.decode('utf-8'), page + 1),
                        headers=self.headers,
                        callback=self.one_parse
                    )
            else:
                r.sadd('name', name.decode('utf-8'))
                break


        # name_list = self.getAnchorId('anchorName')

        # for name in name_list:
        #     totalcounts = self.getTotalCounts(name)
        #     if totalcounts//20 == 0:
        #         num = 1
        #     else:
        #         num = totalcounts//20+1
        #     for page in range(num):
        #         yield scrapy.Request(
        #             url='https://v.taobao.com/micromission/req/selectCreatorV3.do?cateType=701&nick={}&currentPage={}&_output_charset=UTF-8&_input_charset=UTF-8'.format(name.decode('utf-8'), page + 1),
        #             headers=self.headers,
        #             callback=self.one_parse
        #         )

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
            raise CloseSpider('cookie已过期')

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
