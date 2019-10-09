# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient


class Dp92Pipeline(object):
    def process_item(self, item, spider):
        return item

class Dp92MongoDBPipeline(object):
    collection = '92dp_Data'
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
        print(spider.name)
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self,spider):
        self.client.close()

    def process_item(self,item,spider):
        res = self.db[self.collection].find_one({"video_url": item.get('video_url')})
        if not res:
            data = {
                "Classification_one": item['Classification_one'],
                "Classification_two": item['Classification_two'],
                'Classification_three': item['Classification_three'],
                "title": item['title'],
                "Commentator": item['Commentator'],
                'Commentator_lv': item['Commentator_lv'],
                "Comment": item['Comment'],
                "BrandName": item['BrandName'],
                'CommodityName': item['CommodityName'],
                "video_url": item['video_url'],
                "Views_num": item['Views_num'],
                # 'comment_num': item['comment_num'],
                'concerns_num': item['concerns_num'],

            }
            self.db[self.collection].insert_one(data)
            return item
