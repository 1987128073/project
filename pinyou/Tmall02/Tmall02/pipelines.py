# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import time

import redis
from pymongo import MongoClient


class Tmall02Pipeline(object):
    def process_item(self, item, spider):
        return item

class CsvPipeline1(object):
    def __init__(self):
        self.f = open("goodsid-uid.csv", "a+", encoding='utf-8',newline='')
        self.writer = csv.writer(self.f)
        self.writer.writerow(['商品ID', 'UID'])

    def process_item(self, item, spider):
        goods = [item['goodsid'], item['uid']]

        self.writer.writerow(goods)
        return item

    def close_spider(self, spider):  # 关闭
        self.f.close()

class MongoDBPipeline(object):
    collection = 'data_goods'
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
            'goodsid': item['goodsid'],
            'keyword': item['keyword']
        }
        table = self.db[self.collection]
        table.insert_one(data)
        return item

class AnchoridspiderMongoDBPipeline(object):
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
        self.redis = redis.StrictRedis(host='192.168.1.45', port=6379, db=0, password='admin')
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.time_str+self.collection_dict[spider.name]]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if spider.name == 'tb_anchor_goods':
            self.process_anchor_goods(item)
        elif spider.name == 'tb_anchor':
            self.process_anchor(item)
        elif spider.name == 'aid':
            self.process_id_to_redis(item)
            self.process_anchorid(item)
        elif spider.name == 'tb':
            self.process_shopid(item)

    def process_anchor_goods(self, item):
        # res = self.collection.find_one({"accountId": item.get('accountId')})
        pass

    def process_anchor(self, item):
        res = self.collection.find_one({"accountId": item.get('accountId')})
        if not res:
            data = {
                "accountId": item['accountId'],
                "accountName": item['accountName'],
                'fansNum': item['fansNum'],
                'headImg_url': item['headImg_url'],
                "alliveId": item['alliveId'],
                "allpv": item['allpv'],
                'alluv': item['alluv'],
                'countitemId': item['countitemId'],
                "countshopId": item['countshopId'],
                "evepv": item['evepv'],
                'eveuv': item['eveuv'],
                'liveId': item['liveId'],
                'evetaobaoclass2scale': item['evetaobaoclass2scale'],
                'create_time': time.strftime("%Y-%m-%d", time.localtime())
            }
            self.collection.insert_one(data)
            return item

    def process_anchorid(self, item):
        res = self.collection.find_one({"anchorId": item.get('anchorId')})
        if not res:
            data = {
                "anchorId": item['anchorId'],
            }
            self.collection.insert_one(data)
            return item

    def process_shopid(self, item):
        res = self.collection.find_one({"shopId": item.get('shopId')})
        if not res:
            data = {
                "shopId": item['shopid'],
            }
            self.collection.insert_one(data)
            return item

    def process_id_to_redis(self, item):
        self.redis.sadd('anchorId', item['anchorId'])
        return item