from pymongo import MongoClient
from config import environments


def conn_mongo(mongo_url, db_name, collection_name):
    clent = MongoClient(mongo_url)
    db = clent[db_name]
    collection = db[collection_name]
    return collection


def update_mongo():
    env_dict = environments.get('dev')
    clent = MongoClient(env_dict.get('mongodb_host'), port=env_dict.get('mongodb_port'))
    db = clent['v3_app_data_parsed']
    save_db = clent['pl_taobao_dataV3']
    for i in db['live_pro_anchor'].find({}):
        res = save_db['live_pro_anchor'].find_one({'_id': f'{i.get("_id")}:{i.get("live_id")}'})
        if not res:
            d = dict(i)
            d['_id'] = f'{i.get("_id")}:{i.get("live_id")}'
            d['item_id'] = i.get("_id")
            save_db['live_pro_anchor'].insert_one(d)


if __name__ == '__main__':
    update_mongo()


