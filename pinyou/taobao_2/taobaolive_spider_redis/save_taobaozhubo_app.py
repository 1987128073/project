from pymongo import MongoClient

db = MongoClient('192.168.1.180', port=32766)['pltaobao']['anchor_app_data']


def save_taobaoanchor_app_data(origin_data):
    resultList = origin_data.get('resultList')
    for result in resultList:
        res = db.find_one({'_id': int(result.get('userId'))})
        if not res:
            data = {
                '_id': int(result.get('userId')),
                'name': result.get('name'),
                'certName': result.get('certName'),
                'city': result.get('city'),
                'fansCount': result.get('fansCount'),
                'headImage': result.get('headImage'),
            }
            print(data)
            db.insert_one(data)
