import csv

import redis
from pymongo import MongoClient

clent = MongoClient('192.168.1.45')
db = clent['pltaobao']


def csv_to_redis():
    filename = 'anchor_analysis_data'
    r = redis.StrictRedis(host='192.168.1.45', port=6379, password='admin', db=0)
    with open(r'C:\Users\Admin\PycharmProjects\pinyou\request-script\file\{}.csv'.format(filename), 'r', encoding='utf-8') as f:
        csv_data = csv.reader(f, dialect='excel')
        for a in csv_data:
            r.sadd('anchorId_liveid', a[1])

def csv_to_mongo(filename):
    clent = MongoClient('192.168.1.45')
    db = clent['pltaobao']
    collection = db['taobao_catId_pl_catId']
    with open(r'C:\Users\Admin\PycharmProjects\pinyou\request-script\file\{}.csv'.format(filename), 'r', encoding='utf-8') as f:
        csv_data = csv.reader(f, dialect='excel')
        for a in csv_data:
            taobaocat_id_two = a[2]
            plcat_id = a[0]

            res = collection.find_one({'taobaocat_Id': taobaocat_id_two, 'plcat_Id': plcat_id})
            if not res:
                data = {
                    'taobaocat_Id': taobaocat_id_two,
                    'plcat_Id': plcat_id
                }
                collection.insert_one(data)


def select_goods_catId(catid, rootid):
    res = db['taobao_catId_pl_catId'].find_one({'taobaocat_Id': str(rootid)})
    if res:
        return res.get('plcat_Id')
    res = db['taobao_catId_pl_catId'].find_one({'taobaocat_Id': str(catid)})
    if res:
        return res.get('plcat_Id')
    return None


def mongo_to_mongo():

    collection = db['all_tb_anchor_goods_tesk']
    collection2 = db['all_tb_anchor_goods_test']
    num = 1

    for item in collection.find():

        if not db['all_tb_anchor_goods_tesk'].find_one({"anchorId": str(item.get('accountId')), 'createTime': item.get('createTime'), "itemId": str(item.get('itemId'))}):
            categoryid = select_goods_catId(item.get('categoryId'), item.get('rootCategoryId'))
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

            collection2.insert_one(data)

            print(num)
            num += 1

def mongod_to_redis(filename):
    clent = MongoClient('192.168.1.45')
    db = clent['pltaobao']
    collection = db['tb_anchor_goods']
    r = redis.StrictRedis(host='192.168.1.45', port=6379, db=0, password='admin')
    with open(r'C:\Users\Admin\PycharmProjects\pinyou\request-script\file\{}.csv'.format(filename), 'r', encoding='utf-8') as f:
        csv_data = csv.reader(f, dialect='excel')
        for a in csv_data:
            data_list = collection.find({'accountId': str(a[0])})
            for data in data_list:
                res = db['tb_anchor_goods_task'].find_one({'accountId': str(data.get('accountId')), 'itemId': str(data.get('itemId')), 'createTime': data.get('createTime')})
                if not res:
                    db['tb_anchor_goods_task'].insert_one(data)

                anchorId = data.get('accountId')
                ItemId = data.get('itemId')
                r.sadd('anchorId:ItemId', '{}:{}'.format(anchorId, ItemId))


def mongod_to_redis_test(filename):
    clent = MongoClient('192.168.1.45')
    db = clent['pltaobao']
    collection = db['tb_anchor_goods_task']
    r = redis.StrictRedis(host='192.168.1.45', port=6379, db=0, password='admin')
    with open(r'C:\Users\Admin\PycharmProjects\pinyou\request-script\file\{}.csv'.format(filename), 'r',
              encoding='utf-8') as f:
        csv_data = csv.reader(f, dialect='excel')
        for a in csv_data:
            data_list = collection.find({'accountId': str(a[0])})
            for data in data_list:
                anchorId = data.get('accountId')
                ItemId = data.get('itemId')
                r.sadd('anchorId:ItemId1', '{}:{}'.format(anchorId, ItemId))

def b(filename):
    clent = MongoClient('192.168.1.45')
    db = clent['pltaobao']
    collection = db['Id_of_live_broadcast_of_anchor']
    r = redis.StrictRedis(host='192.168.1.45', port=6379, db=0, password='admin')
    with open(r'C:\Users\Admin\PycharmProjects\pinyou\request-script\file\{}.csv'.format(filename), 'r',
              encoding='utf-8') as f:
        csv_data = csv.reader(f, dialect='excel')
        for a in csv_data:
            data = collection.find_one({'_id': str(a[0])})
            print(data.get('livelist'))

def a():
    r = redis.StrictRedis().from_url('redis://:PL298CS2@172.81.225.73:6379/1')
    clent = MongoClient('192.168.1.180',port=32766)
    db = clent['pltaobao']
    collection = db['hot_anchor_info']
    res = collection.find()
    for i in res:

        r.sadd('anchorName:RoomId:uid', "{}:{}:{}".format(i.get('anchorName'), i.get('anchorId'), i.get('fansCount')))

if __name__ == '__main__':
    # mongod_to_redis('anchorId')
    # b('anchorId')
    # csv_to_redis()
    a()