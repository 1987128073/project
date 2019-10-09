# import csv
import time

import redis
from pymongo import MongoClient
# r = redis.StrictRedis(host='192.168.1.45', port=6379, db=1, password='admin')
db1 = MongoClient('192.168.1.180', port=32766)['pltaobao']['anchor_info']

db2 = MongoClient('192.168.1.180', port=32766)['v3_app_data_parsed']['anchors']
# db2 = MongoClient('192.168.1.45')['pltaobao']
# # collection = db2['LiveIdData']
# all_data = collection.find()
#
# for data in all_data:
#     r.sadd('anchorId_pop2', f'{data.get("anchorId")}')
#
# for data in all_data:
#     r.sadd('anchorId_pop', f'{data.get("anchorId")}:{data.get("anchorName")}:{data.get("fansCount")}')

# import pymysql
#
# db = pymysql.connect(host='211.159.215.254',  # 数据库服务器IP
#                      port=62787,
#                      user='root',
#                      passwd='dvUJiSr6hn8h',
#                      db='pinliang_test')  # 数据库名称
#
#
# def select_goods_categoryId(catId):
#
#     # 使用cursor()方法创建一个游标对象cur （可以理解为激活数据库）
#     cur = db.cursor()
#
#     # 使用execute()执行SQL语句
#     cur.execute("select category from  pl_taobao_category where tao_leaf_category_id={}".format(catId))
#
#     # 使用 fetchone() 方法获取一条数据
#     data = cur.fetchone()
#
#     if not data:
#         catId = 2337
#     else:
#         catId = data[0]
#
#     # 关闭数据库连接
#
#     return catId
#
# def select_mongo_2337():
#
#
#
#     cur = db2['all_goods_detail'].find({'plcategory': 2337})
#     for i in cur:
#         catId = select_goods_categoryId(int(i.get('categoryId')))
#         db2['all_goods_detail'].update_one({"_id": i.get('_id')}, {'$set': {'plcategory': int(catId)}})
#
#     db.close()
#
# def select_mongo_test():
#     cur = db2['all_tb_anchor_goods_test'].find()
#     for i in cur:
#         catId = select_goods_categoryId(int(i.get('categoryId')))
#         db2['all_goods_detail'].update_one({"_id": i.get('_id')}, {'$set': {'plcategory': int(catId)}})
#
#     db.close()
#
# def select_mongo():
#     num = 0
#     c = 84
#     count = 10000
#     while c:
#
#         cur = db2['all_goods_detail'].find().skip(num * count).limit(count)
#         print(c)
#         num += 1
#         c -= 1
#         for i in cur:
#             catId = select_goods_categoryId(int(i.get('categoryId')))
#             db2['all_goods_detail'].update_one({"_id": i.get('_id')}, {'$set': {'plcategory': int(catId)}})
#
#     db.close()
#
#
# def add_task():
#     num = 0
#     c = 83
#     count = 10000
#     while c:
#
#         cur = db2['all_goods_detail'].find().skip(num*count).limit(count)
#
#         num += 1
#         c -= 1
#         for a in cur:
#             print(a.get("liveId"), a.get("itemId"))
#             res = db2['all_tb_anchor_goods_test'].find_one({'liveId': a.get("liveId"), 'itemId': a.get("itemId")})
#             if not res:
#                 r.sadd('liveId:ItemId', f'{a.get("liveId")}:{a.get("itemId")}')
#


def anchor_info():
    cur = db1.find({})
    for res in cur:

        res2 = db2.find_one({'_id': int(res.get('anchorId'))})
        if not res2:
            data = {
                '_id': int(res.get('anchorId')),
                'room_num': None,
                'nick': res.get('anchorName'),
                'organ_id': None,
                'anchor_type': None,
                'head_image': res.get('anchorPhoto'),
                'create_at': int(time.time()),
                'head_background_image': None,
                'have_into_sql': False

            }
            db2.insert_one(data)


if __name__ == '__main__':
    # select_mongo()
    # add_task()
    anchor_info()
    pass