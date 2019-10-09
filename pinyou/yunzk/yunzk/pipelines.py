# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import time

from pymongo import MongoClient


class YunzkPipeline(object):
    def process_item(self, item, spider):
        return item

class YunzkDataMongoDBPipeline(object):
    # collection = 'YunzkData(ku.iyunzk.com)'
    def __init__(self, mongo_uri, mongo_db, collection_dict):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_dict = collection_dict
        self.time_str = time.strftime("%Y-%m-%d", time.localtime())

    @classmethod
    def from_crawler(cls, crawler):
        '''
            scrapy为我们访问settings提供了这样的一个方法，这里，
            我们需要从settings.py文件中，取得数据库的URI和数据库名称
        '''
        return cls(
        mongo_uri=crawler.settings.get('MONGO_URI'),
        mongo_db=crawler.settings.get('MONGO_DB'),
        collection_dict=crawler.settings.get('COLLECTION')
        )

    def open_spider(self, spider):
        print(spider.name)
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.time_str + self.collection_dict[spider.name]]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if spider.name == 'yzk':
            self.process_yzk(item)
        elif spider.name == 'dataoke':
            self.process_dataoke(item)

    def process_yzk(self, item):
        res = self.collection.find_one({"auction_id": item.get('auction_id')})
        if not res:
            data = {
                # "id": item['id'],
                # "name": item['name'],
                'auction_id': item['auction_id'],
                'title': item['title'],
                "d_title": item['d_title'],
                "intro": item['intro'],
                'pic': item['pic'],
                'sales_num': item['sales_num'],
                "is_tmall": item['is_tmall'],
                "seller_id": item['seller_id'],
                'cid': item['cid'],
                'coupon_id': item['coupon_id'],
                'coupon_price': item['coupon_price'],
                "coupon_end_time": item['coupon_end_time'],
                'coupon_url': item['coupon_url'],
                'add_time': item['add_time'],
                'create_time': item['create_time'],
                'spider_url': 'ku.iyunzk.com'
            }
            self.collection.insert_one(data)
            return item

    def process_dataoke(self, item):
        res = self.collection.find_one({"auction_id": item.get('auction_id')})
        if not res:
            data = {
                # "id": item['id'],
                # "name": item['name'],
                'auction_id': item['auction_id'],
                'title': item['title'],
                "d_title": item['d_title'],
                "intro": item['intro'],
                'pic': item['pic'],
                'sales_num': item['sales_num'],
                "is_tmall": item['is_tmall'],
                "seller_id": item['seller_id'],
                'cid': item['cid'],
                'coupon_id': item['coupon_id'],
                'coupon_price': item['coupon_price'],
                "coupon_end_time": item['coupon_end_time'],
                'coupon_url': item['coupon_url'],
                'add_time': item['add_time'],
                'create_time': item['create_time'],
                'spider_url': 'dataoke.com'
            }
            self.collection.insert_one(data)
            return item