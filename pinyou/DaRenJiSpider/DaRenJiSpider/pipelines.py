# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import time

from pymongo import MongoClient


class DarenjispiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):

    def __init__(self,mongo_uri,mongo_db,collection_dict):
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
        collection_dict = crawler.settings.get('COLLECTION')
        )

    def open_spider(self,spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self,spider):
        self.client.close()

    def process_item(self,item,spider):
        data = {
            "anchorName": item['anchorName'],
            "roomNumber": str(item['roomNumber']),
            'category': item['category'],
            'liveCount': item['liveCount'],
            'cearteTime': self.time_str,
        }
        table = self.db[self.collection_dict[spider.name]]
        table.insert_one(data)
        return item