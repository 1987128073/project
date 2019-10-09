# -*- coding: utf-8 -*-
import csv
import scrapy
from ..items import Tmall_UIDItem

class TmSpider(scrapy.Spider):
    name = 'tm_uid'
    allowed_domains = ['tmall.com','taobao.com']

    def start_requests(self):
        with open('shop.csv', 'r', encoding='utf-8', newline='') as f:
            csv_data = csv.reader(f, dialect='excel')
            for i in csv_data:
                yield scrapy.Request(url=i[3], callback=self.parse)

    def parse(self, response):

        item = Tmall_UIDItem()
        # print(response.request.url)
        if response.request.url[:19] == 'https://item.taobao':
            id = response.request.url.split('?')[1].split('=')[2].split('&')[0]
        else:
            id = response.request.url.split('?')[1].split('=')[1].split('&')[0]
        try:
            uid = response.xpath('//*[@id="J_ShopInfo"]/div/div[1]/div[3]/dl/dd/a/text()').extract_first().strip()
        except:
            uid = response.xpath('//*[@id="shopExtra"]/div[1]/a/strong/text()').extract_first().strip()

        item['goodsid'] = id
        item['uid'] = uid
        # print(id,uid)
        yield item
