# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv

from pymongo import MongoClient


class TmallPipeline(object):
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


class CsvPipeline(object):
    def __init__(self):
        self.f = open("goods_brand_name.csv", "a+", encoding='utf-8', newline='')
        self.writer = csv.writer(self.f)
        self.writer.writerow(['商品ID', '品牌名', '商品参数'])

    def process_item(self, item, spider):
        goods = [item['goodsid'], item['brand_name'], item['info']]
        self.writer.writerow(goods)
        return item

    def close_spider(self, spider):  # 关闭
        self.f.close()


class MongoDBPipeline(object):

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
        res = self.db['goodsInfo_PrimaryData'].find_one({'_id': str(item.get('itemId'))})
        if not res:
            data = {
                '_id': str(item['itemId']),
                'goodsInfo': item['goodsInfo'],
                'is_deal': 0
            }
            table = self.db['goodsInfo_PrimaryData']
            table.insert_one(data)
        return item

    # def process_goodsSellCount(self,item,spider):
    #     res = self.db['goodsSellCount'].find_one({'_id': str(item.get('itemId'))})
    #     if not res:
    #         data = {
    #             '_id': str(item['itemId']),
    #             'goodsInfo': item['goodsInfo']
    #         }
    #         table = self.db['goodsSellCount']
    #         table.insert_one(data)
    #     return item