# -*- coding: utf-8 -*-
import csv
import json
import re
import urllib.parse
from scrapy.http import Request
from scrapy_redis.utils import bytes_to_str
from ..spiders.BaseSpider import BaseSpider
from ..items import Tmall02Item


class TbSeacherSpider(BaseSpider):
    '''
        获取淘宝搜索页不同类目下商品所属商店的ShopId
        '''
    name = 'tbsearch'
    redis_key = 'tbsearchspider:start_urls'

    def make_request_from_data(self, data):
        keyword = bytes_to_str(data)
        url_keyword = urllib.parse.quote(keyword)

        for page in range(1, 101):
            url = 'https://s.taobao.com/search?q={}&js=1&s={}}'.format(url_keyword, (page - 1) * 44)
            yield Request(
                url=url,
                dont_filter=True,
                # meta={
                #     'keyword': keyword
                # }
            )

    def parse(self, response):
        # meta = response.meta
        pattern = re.compile(r'g_page_config = ([\s\S].*) g_srp_loadCss', re.S)
        a = re.search(pattern, response.text).group(1)[:-5]
        r = json.loads(a)
        if r.get('mods').get('itemlist').get('status') == 'show':
            detail_data = r.get('mods').get('itemlist').get('data').get('auctions')
            for data in detail_data:
                detail_url = 'https:' + data.get('detail_url')

                yield Request(
                    url=detail_url,
                    dont_filter=True,
                    # meta={
                    #     'keyword': keyword
                    # }
                    callback=self.parse_two
                )

    def parse_two(self, response):
        shopid = response.xpath('/html/head/meta[@name="microscope-data"]/@content').extract_first().split(';')[3].split('=')[1]
        TBShopid = Tmall02Item()
        TBShopid['shopid'] = shopid
        yield TBShopid