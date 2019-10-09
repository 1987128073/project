# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import time

from pymongo import MongoClient

from .items import couponItem

class GoodsdataPipeline(object):
    def process_item(self, item, spider):
        return item

class TbMongoDBPipeline(object):
    time_str = time.strftime("%Y-%m-%d", time.localtime())
    collection = '{}_data_goods'.format(time_str)
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        '''
            scrapy为我们访问settings提供了这样的一个方法，这里，
            我们需要从settings.py文件中，取得数据库的URI和数据库名称
        '''
        return cls(
        mongo_uri=crawler.settings.get('MONGO_URI'),
        mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self,spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self,spider):
        self.client.close()

    def process_item(self,item,spider):
        data = {
            "category": item['category'],
            "commission_rate": item['commission_rate'],
            'coupon_click_url': item['coupon_click_url'],
            'coupon_end_time': item['coupon_end_time'],
            'coupon_info': item['coupon_info'],
            'coupon_remain_count': item['coupon_remain_count'],
            'coupon_start_time': item['coupon_start_time'],
            'coupon_total_count': item['coupon_total_count'],
            'item_description': item['item_description'],
            'item_url': item['item_url'],
            'nick': item['nick'],
            'num_iid': item['num_iid'],
            'pict_url': item['pict_url'],
            'seller_id': item['seller_id'],
            'shop_title': item['shop_title'],
            'title': item['title'],
            'user_type': item['user_type'],
            'volume': item['volume'],
            'zk_final_price': item['zk_final_price'],

        }
        table = self.db[self.collection]
        table.insert_one(data)
        return item