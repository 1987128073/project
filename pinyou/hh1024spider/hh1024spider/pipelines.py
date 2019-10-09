# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import time

import redis
from pymongo import MongoClient


class Hh1024SpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class Hh1024SpiderMongoDBPipeline(object):

    def __init__(self, mongo_uri, mongo_db, collection_dict, mongo_port):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_port = mongo_port
        self.collection_dict = collection_dict

    @classmethod
    def from_crawler(cls, crawler):
        '''
            scrapy为我们访问settings提供了这样的一个方法，这里，
            我们需要从settings.py文件中，取得数据库的URI和数据库名称
        '''
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
            collection_dict=crawler.settings.get('COLLECTION'),
            mongo_port=crawler.settings.get('MONGO_PORT')
        )

    def open_spider(self, spider):
        print(spider.name)
        self.redis = redis.StrictRedis(host='192.168.1.45', port=6379, db=0, password='admin')
        self.client = MongoClient(self.mongo_uri, port=self.mongo_port)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.collection_dict[spider.name]]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if spider.name == 'hh1024LivelistAPI':
            self.process_goods_info(item)
        elif spider.name == 'hh1024AnchorAPI':
            self.process_anchor_goods_info(item)

    def process_goods_info(self, item):
        res = self.collection.find_one({"itemId": str(item.get('itemId'))})
        if not res:
            data = {

                'itemId': str(item.get('itemId')),
                'itemUrl': item.get('itemUrl'),
                'pictUrl': item.get('pictUrl'),
                'reservePrice': item.get('reservePrice'),
                'title': item.get('title'),
            }
            self.collection.insert_one(data)  # 插入一条不存在的主播数据
        return item

    def process_anchor_goods_info(self, item):
        res = self.collection.find_one({"anchorId": str(item.get('anchorId'))})
        if not res:
            data = {
                'anchorId': str(item.get('anchorId')),
                'With_cargo_goods': item.get('With_cargo_goods'),
                'is_deal': 0,  # 0表示未处理，1表示已处理
                'create_time': time.strftime("%Y-%m-%d", time.localtime()),
            }
            self.collection.insert_one(data)
        else:
            if res.get('With_cargo_goods') == item.get('With_cargo_goods'):
                pass
            else:
                self.collection.update_one({'anchorId': str(id)},
                                           {'$set':
                                               {
                                                   'With_cargo_goods': item.get('With_cargo_goods'),

                                               }
                                           }
                                           )
        return item

    def process_itemId(self, item):
        res = self.collection.find_one({"itemId": item.get('itemId')})
        if not res:
            data = {
                "anchorId": item['anchorId'],
            }
            self.collection.insert_one(data)
            return item


    def process_id_to_redis(self, item):
        self.redis.sadd('anchorId', item['anchorId'])
        return item
