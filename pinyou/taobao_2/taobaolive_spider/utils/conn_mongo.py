from pymongo import MongoClient

def conn_mongo(mongo_url, db_name, collection_name):
    clent = MongoClient(mongo_url)
    db = clent[db_name]
    collection = db[collection_name]
    return collection
