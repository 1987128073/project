# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider


class DarenjiSpider(RedisSpider):
    name = 'darenji'
    allowed_domains = ['darenji.com']
    redis_key = 'darenji:start_urls'

    def parse(self, response):
        response.xpath('//*[@id="types"]').extract_first()
