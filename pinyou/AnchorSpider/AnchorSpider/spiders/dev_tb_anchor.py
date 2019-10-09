# -*- coding: utf-8 -*-
import datetime
import json
import redis
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.utils.project import get_project_settings
from ..items import DevAnchorspiderItem


class TbAnchorSpider(scrapy.Spider):
    name = 'dev_tb_anchor'
    allowed_domains = ['zhiboshuju.com']

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
                callback=self.parse
            )

    def parse(self, response):
        json_obj = json.loads(response.text).get('data')
        if json_obj:
            anchorspiderItem = DevAnchorspiderItem()
            anchorspiderItem['anchorId'] = json_obj.get('accountId')
            anchorspiderItem['anchorName'] = json_obj.get('accountName')
            anchorspiderItem['fansCount'] = json_obj.get('fansNum')
            anchorspiderItem['anchorPhoto'] = json_obj.get('headImg')
            yield anchorspiderItem