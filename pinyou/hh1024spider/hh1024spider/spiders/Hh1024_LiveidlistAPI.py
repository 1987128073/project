# -*- coding: utf-8 -*-
import hashlib
import json
import time

import redis
import scrapy
from scrapy.utils.project import get_project_settings

from ..items import hh1024LivelistAPI as Item


class Hh1024Spider(scrapy.Spider):
    name = 'hh1024LivelistAPI'
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
        while 1:
            liveId = r.spop('liveId')
            if not liveId:
                break
            param = {
                "itemEntry": {"liveIdList": [liveId.decode('utf-8')]},
                'pageEntry': {"pageSize":500,"pageNum":1,"sortBy":1}
            }
            params = {
                "tenant": "caihui",
                "timestamp": self.timestamp,
                "token": self.settings.get('TOKEN'),
                "sign": self.data_sha256(param),
                "param": param
            }
            yield scrapy.FormRequest(
                url='https://do.comfire.cn/caihui/liveInfo/getGoodsList',
                method='post',
                formdata=json.dumps(params),
                dont_filter=True,
                callback=self.parse
            )

    def parse(self, response):
        json_obj = json.loads(response.text).get('results')
        if json_obj:
            for data in json_obj:
                item = Item()
                item['itemId'] = data.get('itemId')
                item['itemUrl'] = data.get('itemUrl')
                item['pictUrl'] = data.get('pictUrl')
                item['reservePrice'] = data.get('reservePrice')
                item['title'] = data.get('title')

                yield item
