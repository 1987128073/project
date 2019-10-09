# -*- coding: utf-8 -*-
import csv
import scrapy
from ..items import TmallItem, TmallItemBrandname


class TmSpider(scrapy.Spider):
    name = 'tm'
    allowed_domains = ['tmall.com']

    def start_requests(self):
        with open(r'C:\Users\Admin\PycharmProjects\pinyou\Tmall\Tmall\file\1.csv', 'r', encoding='utf-8', newline='') as f:
            csv_data = csv.reader(f, dialect='excel')
            for i in csv_data:
                yield scrapy.Request(url=i[0], callback=self.parse)

    def parse(self, response):
        status = response.status
        if status not in [302, 301]:
            item = TmallItemBrandname()
            id = response.request.url.split('?')[1].split('=')[1].split('&')[0]
            # print(response.xpath('//*[@id="J_attrBrandName"]').extract())
            try:
                brand_name = response.xpath('//*[@id="J_attrBrandName"]/text()').extract()[0].split(r'\xa0')[1]
            except:
                brand_name = ''
            print(response.xpath('//*[@id="J_AttrUL"/text()]').extract())
            info = response.xpath('//*[@id="J_AttrUL"]').extract()[0].strip()
            item['goodsid'] = id
            item['brand_name'] = brand_name
            item['info'] = info

            yield item
