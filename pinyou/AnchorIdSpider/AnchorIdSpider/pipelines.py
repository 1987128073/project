# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import time

import redis
from pymongo import MongoClient


class AnchoridspiderPipeline(object):
    def process_item(self, item, spider):
        return item

class AnchoridspiderMongoDBPipeline(object):
    # collection = 'YunzkData(ku.iyunzk.com)'
    def __init__(self, mongo_uri, mongo_db, collection_dict, mongo_port):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_port = mongo_port
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
        if spider.name == 'tb_anchor_goods':
            self.process_anchor_goods(item)
        elif spider.name == 'tb_anchor':
            self.process_anchor(item)
        elif spider.name == 'tbshop':
            self.process_id_to_redis(item)
            # self.process_anchor(item)
        elif spider.name == 'search_aid':
            self.process_id_to_redis(item)
        elif spider.name == 'aliVsessionAnchor':
            self.process_id_to_redis(item)
            self.process_anchor(item)
        elif spider.name == 'searchAnchorAnchorIdAPI':
            self.process_id_to_redis(item)
            self.process_anchor(item)
        elif spider.name == 'fansFeature':
            self.process_anchorfansFeature(item)
        elif spider.name == 'searchAnchorAPI':
            self.process_id_to_redis(item)
            self.process_anchor(item)
        elif spider.name == 'organ_info':
            self.process_organ(item)

    def process_anchor_goods(self, item):
        # res = self.collection.find_one({"accountId": item.get('accountId')})

        anchor = dict(item)
        anchor['accountId'] = item.get('accountId')
        anchor['accountName'] = item.get('accountName')
        anchor['title'] = item.get('title')
        anchor['createTime'] = item.get('createTime')
        anchor['itemId'] = item.get('itemId')
        anchor['sellerId'] = item.get('sellerId')
        anchor['goods_url'] = item.get('goods_url')
        anchor['shopName'] = item.get('shopName')
        anchor['liveId'] = item.get('liveId')
        anchor['liveURL'] = item.get('liveURL')
        anchor['livePrice'] = item.get('livePrice')
        anchor['categoryId'] = item.get('categoryId')
        anchor['class2name'] = item.get('class2name')
        anchor['shopId'] = item.get('shopId')
        anchor['shopType'] = item.get('shopType')
        anchor['maintype'] = item.get('maintype')
        anchor['rootCategoryId'] = item.get('rootCategoryId')
        self.collection.insert_one(anchor)
        return item

    def process_anchor(self, item):
        res = self.collection.find_one({"anchorId": str(item.get('anchorId'))})
        try:
            darenScore = int(item.get('darenScore'))
        except:
            darenScore = None

        try:
            fansCount = int(item.get('fansCount'))
        except:
            fansCount = None
        if not res:
            data = {

                'anchorId': str(item.get('anchorId')),
                'anchorName': item.get('anchorName'),
                'houseId': None,
                'fansCount': fansCount,
                'liveCount': None,
                'city': item.get('city'),
                'creatorType': item.get('creatorType'),
                'darenScore': darenScore,
                'descText': item.get('descText'),
                'anchorPhoto': item.get('anchorPhoto'),
                'organId': item.get('organId'),
                'fansFeature': None,
                'historyData': None,
                'servType': item.get('servType'),
            }
            self.collection.insert_one(data)  # 插入一条不存在的主播数据
        else:
            try:
                servType = res.get('servType')
            except:
                servType = -1
            if res.get('fansCount') == fansCount and res.get('anchorPhoto') == item.get('anchorPhoto') and res.get('anchorName') == item.get('anchorName') and res.get('city') == item.get('city') and res.get('creatorType') == item.get('creatorType') and res.get('darenScore') == darenScore and res.get('organId') == item.get('organId') and servType == item.get('servType'):
                pass
            else:
                self.collection.update_one({'anchorId': str(id)},
                                           {'$set':
                                                {
                                                    'fansCount': fansCount,
                                                    'anchorName': item.get('anchorName'),
                                                    'city': item.get('city'),
                                                    'creatorType': item.get('creatorType'),
                                                    'darenScore': darenScore,
                                                    'descText': item.get('descText'),
                                                    'anchorPhoto': item.get('anchorPhoto'),
                                                    'organId': item.get('organId'),
                                                    'servType': item.get('servType')
                                                }
                                           }
                                           )  # 更新已存在的主播数据
        return item

    def process_anchorid(self, item):
        res = self.collection.find_one({"anchorId": item.get('anchorId')})
        if not res:
            data = {
                "anchorId": item['anchorId'],
            }
            self.collection.insert_one(data)
            return item

    def process_anchorfansFeature(self, item):
        res = self.collection.find_one({"anchorId": item.get('anchorId')})
        if not res:

            data = {
                "anchorId": str(item['anchorId']),
                'age': item['age'],
                'area': item['area'],
                'career': item['career'],
                'cate': item['cate'],
                'gender': item['gender'],
                'interest': item['interest']
            }
            self.collection.insert_one(data)
        else:
            if res.get('area') == item.get('area') and res.get('area') == item.get('area') and res.get('career') == item.get(
                    'career') and res.get('cate') == item.get('cate') and res.get('gender') == item.get(
                    'gender') and res.get('interest') == item.get(
                    'interest'):
                pass
            else:
                self.collection.update_one({'anchorId': str(id)},
                                           {'$set':
                                               {
                                                   'age': item.get('age'),
                                                   'area': item.get('area'),
                                                   'career': item.get('career'),
                                                   'cate': item.get('cate'),
                                                   'gender': item.get('gender'),
                                                   'interest': item.get('interest'),
                                               }
                                           }
                                           )
        return item

    def process_id_to_redis(self, item):
        self.redis.sadd('anchorId', item['anchorId'])
        return item

    def process_organ(self, item):
        res = self.collection.find_one({"_id": str(item.get('organId'))})
        try:
            darenCount = int(item.get('darenCount'))
        except:
            darenCount = None

        try:
            topdrenCount = int(item.get('topdrenCount'))
        except:
            topdrenCount = None

        try:
            compositeScore = int(item.get('compositeScore'))
        except:
            compositeScore = None

        if not res:
            data = {

                '_id': str(item.get('organId')),
                'organText': item.get('organText'),
                'organName': item.get('organName'),
                'agencyPhoto': item.get('agencyPhoto'),
                'tag': item.get('tag'),
                'catetgory': item.get('catetgory'),
                'darenCount': darenCount,
                'topdrenCount': topdrenCount,
                'compositeScore': compositeScore,
                'verticalField': item.get('verticalField'),
                'platform': 1,
            }
            self.collection.insert_one(data)  # 插入一条不存在的主播数据
        else:
            if res.get('organText') == item.get('organText') and res.get('organName') == item.get('organName') and res.get(
                    'agencyPhoto') == item.get('agencyPhoto') and res.get('tag') == item.get('tag') and res.get(
                    'catetgory') == item.get('catetgory') and res.get('darenCount') == darenCount and res.get(
                    'topdrenCount') == topdrenCount and res.get('compositeScore') == compositeScore and res.get(
                    'verticalField') == item.get('verticalField'):
                pass
            else:
                self.collection.update_one({'_id': str(id)},
                                           {'$set':
                                               {
                                                   'organText': item.get('organText'),
                                                   'organName': item.get('organName'),
                                                   'agencyPhoto': item.get('agencyPhoto'),
                                                   'tag': item.get('tag'),
                                                   'catetgory':item.get('catetgory'),
                                                   'darenCount': darenCount,
                                                   'topdrenCount': topdrenCount,
                                                   'compositeScore': compositeScore,
                                                   'verticalField': item.get('verticalField')
                                               }
                                           }
                                           )  # 更新已存在的机构数据
        return item
