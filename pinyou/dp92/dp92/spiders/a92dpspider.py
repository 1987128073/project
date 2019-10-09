# -*- coding: utf-8 -*-
import logging

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import Dp92Item


class A92dpspiderSpider(CrawlSpider):
    name = '92dpspider'
    allowed_domains = ['92dp.com']
    start_urls = ['http://92dp.com/dianping/']

    rules = (
        Rule(LinkExtractor(allow=r'/dianping/\d+-\d+-\d+-\d+\.htm'), follow=True),
        Rule(LinkExtractor(allow=r'/dianping/\d+\.htm'), callback='parse_detail', follow=False),
    )

    def parse_detail(self, response):
        item = Dp92Item()
        item['Classification_one'] = response.xpath('/html/body/div[2]/ol/li[3]/a/text()').extract_first()
        item['Classification_two'] = response.xpath('/html/body/div[2]/ol/li[4]/a/text()').extract_first()
        item['Classification_three'] = response.xpath('/html/body/div[2]/ol/li[5]/a/text()').extract_first()
        item['title'] = response.xpath('/html/body/div[2]/div/div[1]/div[3]/h1/text()').extract_first()
        item['Commentator'] = response.xpath('/html/body/div[2]/div/div[1]/div[3]/div/div[1]/div/div/a/text()').extract_first()
        item['Commentator_lv'] = response.xpath('/html/body/div[2]/div/div[1]/div[4]/text()[2]').extract_first()
        item['Comment'] = response.xpath('/html/body/div[2]/div/div[1]/div[4]/span[5]/text()').extract_first()
        item['BrandName'] = response.xpath('/html/body/div[2]/div/div[1]/div[4]/a[2]/text()').extract_first()
        item['CommodityName'] = response.xpath('/html/body/div[2]/div/div[1]/div[4]/a[3]/text()').extract_first()
        try:
            item['video_url'] = response.xpath('//*[@id="video-player-html5"]/source[2]/@src').extract_first()
        except Exception as e:
            item['video_url'] = response.xpath('//*[@id="video-player-html5"]/source[1]/@src').extract_first()
        item['Views_num'] = response.xpath('/html/body/div[2]/div/div[1]/div[3]/div/div[2]/p[1]/text()').extract_first()[:-4]
        # item['comment_num'] = response.xpath('/html/body/div[2]/div/div[1]/div[5]/form/div[1]/span/text()').extract_first()[3:-1]
        item['concerns_num'] = response.xpath('/html/body/div[2]/div/div[1]/div[3]/div/div[1]/div/div/span/span/text()').extract_first()
        yield item

