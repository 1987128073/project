# -*- coding: utf-8 -*-
import json
import redis
import requests
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.utils.project import get_project_settings
from ..items import AnchoridspiderItem


class TbAnchorSpider(scrapy.Spider):
    name = 'search_aid'
    allowed_domains = ['zhiboshuju.com']

    def start_requests(self):
        settings = get_project_settings()
        r = redis.StrictRedis(host=settings.get('REDIS_IP'), port=settings.get('REDIS_PORT'), db=0,
                              password=settings.get('REDIS_PASSWORD'))
        NAME_LIST = r.smembers('AnchorNickname1')
        for i in NAME_LIST:
            postdata = {
                'accountName': i.decode('utf-8'),
                'openId': 'ofYto04ZtE57zTesjffxdeWmZzQQ'
            }
            yield scrapy.FormRequest(
                url='https://www.zhiboshuju.com/shopanchorWeChat/selectanchotName',
                method='post',
                formdata=postdata,
                dont_filter=True,
                callback=self.parse
            )

    def parse(self, response):
        json_obj = json.loads(response.text).get('data')

        if json_obj:
            for data in json_obj:
                anchorspiderItem = AnchoridspiderItem()
                anchorspiderItem['anchorId'] = data.get('accountId')
                yield anchorspiderItem
