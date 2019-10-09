# -*- coding: utf-8 -*-
import hashlib
import json
import time

import redis
import scrapy
from scrapy.utils.project import get_project_settings
from ..items import hh1024AnchorAPIItem as Item


class Hh1024Spider(scrapy.Spider):
    name = 'hh1024AnchorAPI'
    allowed_domains = ['search_anchor_info.com']
    settings = get_project_settings()
    headers = {
        'Content-Type': 'application/json;charset=UTF-8', 'ETag': '1387aa53', 'Referer': 'https://www.hh1024.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    }

    timestamp = int(time.time() * 1000)

    def data_sha256(self, param):
        s = 'param' + str(param) + '&timestamp=' + str(self.timestamp) + '&tenant=caihui&token=' + self.settings.get('TOKEN')
        sha = hashlib.sha256()
        sha.update(s.encode())
        sign = sha.hexdigest()
        return sign

    def start_requests(self):
        r = redis.StrictRedis(host=self.settings.get('REDIS_IP'), port=self.settings.get('REDIS_PORT'), db=0,
                              password=self.settings.get('REDIS_PASSWORD'))
        for anchorId in r.smembers('anchorId'):

            param = {
                "anchorLiveHistoryEntry": {"anchorId": str(anchorId.decode('utf-8')), "days": 30}
            }
            params = {
                "tenant": "caihui",
                "timestamp": self.timestamp,
                "token": self.settings.get('TOKEN'),
                "sign": self.data_sha256(param),
                "param": param
            }
            yield scrapy.FormRequest(
                url='https://do.comfire.cn/caihui/anchor/getAnchorHistoryInfo',
                method='post',
                formdata=json.dumps(params),
                dont_filter=True,
                meta={'anchorId':anchorId.decode('utf-8')},
                callback=self.one_parse
            )

    def one_parse(self, response):
        anchorId = response.meta.get('anchorId')
        json_obj = json.loads(response.text).get('preload')
        if json_obj.get('result') and json_obj.get('result').get('liveScene'):
            liveIdList = json_obj.get('result').get('liveIdList')
            param = {
                "itemEntry": {"liveIdList": liveIdList},
                'pageEntry': {"pageSize":20,"pageNum":1,"sortBy":1}
            }
            params = {
                "tenant": "caihui",
                "timestamp": self.timestamp,
                "token": self.settings.get('TOKEN'),
                "sign": self.data_sha256(param),
                "param": param
            }
            yield scrapy.FormRequest(
                url='https://do.comfire.cn/caihui/anchor/getAnchorHistoryInfo',
                method='post',
                formdata=params,
                dont_filter=True,
                callback=self.one_parse
            )
            yield scrapy.FormRequest(
                url='https://do.comfire.cn/caihui/anchor/getAnchorHistoryInfo',
                method='post',
                formdata=json.dumps(params),
                meta={'anchorId': anchorId.decode('utf-8')},
                dont_filter=True,
                callback=self.one_parse
            )

    def parse(self, response):
        anchorId = response.meta.get('anchorId')
        json_obj = json.loads(response.text).get('results')
        if json_obj:
            item = Item()
            item['anchorId'] = anchorId
            item['With_cargo_goods'] = json_obj

            yield item
