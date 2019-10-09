# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import time

import redis
from pymongo import MongoClient
from scrapy.utils.project import get_project_settings


class AnchorspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class CsvPipeline(object):
    def __init__(self):
        self.f = open("anchor_data.csv", "a+", encoding='utf-8', newline='')
        self.writer = csv.writer(self.f)
        self.writer.writerow(['userId', 'nick', 'fansCount'])

    def process_item(self, item, spider):
        goods = [item['userId'], item['nick'], item['fansCount']]

        self.writer.writerow(goods)
        return item

    def close_spider(self, spider):  # 关闭
        self.f.close()


class AnchorMongoDBPipeline(object):
    collection = 'anchor_data'
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
            "userId": item['userId'],
            "nick": item['nick'],
            'fansCount': item['fansCount'],

        }
        table = self.db[self.collection]
        table.insert_one(data)
        return item

class AnchorDataMongoDBPipeline(object):
    # collection = 'YunzkData(ku.iyunzk.com)'
    def __init__(self, mongo_uri, mongo_db, collection_dict, catId):
        self.catId = catId
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_dict = collection_dict
        self.time_str = time.strftime("%Y-%m-%d", time.localtime())
        self.setting = get_project_settings()
        self.r = redis.StrictRedis(host=self.setting.get('REDIS_IP'), port=self.setting.get('REDIS_PORT'), db=0,
                              password=self.setting.get('REDIS_PASSWORD'))

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
        catId = crawler.settings.get('Category')
        )

    def open_spider(self, spider):
        print(spider.name)
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection = self.db[self.collection_dict[spider.name]]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if spider.name == 'tb_anchor_goods':
            self.process_anchor_goods(item)
        elif spider.name == 'tb_anchor':
            self.process_anchor(item)
        elif spider.name == 'tb_anchorid':
            self.process_anchorid(item)
        elif spider.name == 'dev_tb_anchor':
            self.process_dev_anchor(item)
        elif spider.name == 'tb_anchor_goods_task':
            self.process_tb_anchor_goods_task(item)

    def process_anchor_goods(self, item):
        res = self.collection.find_one({"anchorId": item.get('accountId'), 'createTime':item.get('createTime'), "itemId": item.get('itemId')})
        if not res:
            categoryid = self.catId.get(item.get('categoryId'))
            if not categoryid:
                categoryid = self.catId.get(item.get('rootCategoryId'))

            if not categoryid:
                categoryid = None
            data = {
                'anchorId': item.get('accountId'),
                'anchorName': item.get('accountName'),
                'title': item.get('title'),
                'createTime': item.get('createTime'),
                'itemId': item.get('itemId'),
                'sellerId': item.get('sellerId'),
                'goods_url': item.get('goods_url'),
                'shopName': item.get('shopName'),
                'liveId': item.get('liveId'),
                'liveURL': item.get('liveURL'),
                'livePrice': item.get('livePrice'),
                'categoryId': item.get('categoryId'),
                'class2name': item.get('class2name'),
                'shopId': item.get('shopId'),
                'shopType': item.get('shopType'),
                'maintype': item.get('maintype'),
                'rootCategoryId': item.get('rootCategoryId'),
                "Monthly_payment": None,
                "CommtentCount": None,
                'is_dispose': 1,
                'plcategory': categoryid
            }

            self.collection.insert_one(data)
            self.r.sadd('ALL_liveId:ItemId', '{}:{}'.format(item.get('liveId'), item.get('itemId')))
            return item

    def process_anchor(self, item):
        res = self.collection.find_one({"accountId": item.get('accountId')})
        try:
            fanscount = int(item.get('fansCount'))
        except:
            fanscount = None

        if not res:
            data = {
                "accountId": item['accountId'],
                "accountName": item['accountName'],
                'fansNum': fanscount,
                'headImg_url': item['headImg_url'],
                "alliveId": int(item['alliveId']),
                "allpv": int(item['allpv']),
                'alluv': int(item['alluv']),
                'countitemId': int(item['countitemId']),
                "countshopId": int(item['countshopId']),
                "evepv": int(item['evepv']),
                'eveuv': int(item['eveuv']),
                'liveId': item['liveId'],
                'evetaobaoclass2scale': item['evetaobaoclass2scale'],
                'create_time': time.strftime("%Y-%m-%d", time.localtime())
            }
            self.collection.insert_one(data)
        else:
            if res.get('fansNum') == fanscount and res.get('headImg_url') == item.get('headImg_url') and res.get(
                    'alliveId') == item.get('alliveId') and res.get('allpv') == item.get('allpv') and res.get(
                    'alluv') == item.get('alluv') and res.get('countitemId') == item.get('countitemId') and res.get(
                    'countshopId') == item.get('countshopId') and res.get('evepv') == item.get('evepv') and res.get(
                    'eveuv') == item.get('eveuv') and res.get('liveId') == item.get('liveId') and res.get(
                    'evetaobaoclass2scale') == item.get('evetaobaoclass2scale'):
                pass
            else:
                self.collection.update_one({'anchorId': str(id)},
                                           {'$set':
                                               {
                                                   'fansNum': fanscount,
                                                    'headImg_url': item['headImg_url'],
                                                    "alliveId": int(item['alliveId']),
                                                    "allpv": int(item['allpv']),
                                                    'alluv': int(item['alluv']),
                                                    'countitemId': int(item['countitemId']),
                                                    "countshopId": int(item['countshopId']),
                                                    "evepv": int(item['evepv']),
                                                    'eveuv': int(item['eveuv']),
                                                    'liveId': item['liveId'],
                                                    'evetaobaoclass2scale': item['evetaobaoclass2scale'],
                                               }
                                           }
                                           )  # 更新已存在的主播数据
        return item

    def process_dev_anchor(self, item):
        res = self.collection.find_one({"anchorId": item.get('accountId')})
        try:
            fanscount = int(item.get('fansCount'))
        except:
            fanscount = None

        if not res:
            data = {

                'anchorId': str(item.get('anchorId')),
                'anchorName': item.get('anchorName'),
                'houseId': None,
                'fansCount': fanscount,
                'liveCount': None,
                'city': None,
                'creatorType': None,
                'darenScore': None,
                'descText': None,
                'anchorPhoto': item['anchorPhoto'],
                'organId': None,
                'fansFeature': None,
                'historyData': None,
            }
            self.collection.insert_one(data)  # 插入一条不存在的主播数据
            return item

    def process_anchorid(self, item):
        res = self.collection.find_one({"anchorId": item.get('anchorId')})
        if not res:
            data = {
                "anchorId": item['anchorId'],
                "anchorName": item['anchorName'],
                'anchorPicture': item['anchorPicture'],
                'endLiveTime': item['endLiveTime'],
                "goodsIndex": item['goodsIndex'],
                "itemId": item['itemId'],
                'startLiveTime': item['startLiveTime'],
                'topic': item['topic'],
            }
            self.collection.insert_one(data)
            return item

    def process_tb_anchor_goods_task(self, item):
        res = self.collection.find_one(
            {"anchorId": item.get('accountId'), 'createTime': item.get('createTime'), "itemId": item.get('itemId')})
        if not res:

            categoryid = self.catId.get(item.get('categoryId'))
            if not categoryid:
                categoryid = self.catId.get(item.get('rootCategoryId'))

            if not categoryid:
                categoryid = None

            data = {
                'anchorId': item.get('accountId'),
                'anchorName': item.get('accountName'),
                'title': item.get('title'),
                'createTime': item.get('createTime'),
                'itemId': item.get('itemId'),
                'sellerId': item.get('sellerId'),
                'goods_url': item.get('goods_url'),
                'shopName': item.get('shopName'),
                'liveId': item.get('liveId'),
                'liveURL': item.get('liveURL'),
                'livePrice': item.get('livePrice'),
                'categoryId': item.get('categoryId'),
                'class2name': item.get('class2name'),
                'shopId': item.get('shopId'),
                'shopType': item.get('shopType'),
                'maintype': item.get('maintype'),
                'rootCategoryId': item.get('rootCategoryId'),
                "Monthly_payment": None,
                "CommtentCount": None,
                'is_dispose': 1,
                'plcategory': categoryid
            }

            self.collection.insert_one(data)
            self.r.sadd('liveId:ItemId', '{}:{}'.format(item.get('liveId'), item.get('itemId')))
            return item


