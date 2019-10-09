from pymongo import MongoClient


def insert_m():
    client = MongoClient(host='192.168.1.51')
    db = client['pltaobao']
    collection01 = db['2019-08-13tb_anchor']
    collection02 = db['tb_anchor']
    for i in collection01.find({}):
        res = collection02.find_one({"accountId": i.get('accountId')})
        if not res:
            data = {
                "accountId": i['accountId'],
                "accountName": i['accountName'],
                'fansNum': int(i['fansNum']),
                'headImg_url': i['headImg_url'],
                "alliveId": i['alliveId'],
                "allpv": int(i['allpv']),
                'alluv': int(i['alluv']),
                'countitemId': int(i['countitemId']),
                "countshopId": int(i['countshopId']),
                "evepv": int(i['evepv']),
                'eveuv': int(i['eveuv']),
                'liveId': i['liveId'],
                'evetaobaoclass2scale': i['evetaobaoclass2scale'],
                'create_time': i['create_time']
            }
            collection02.insert_one(data)

def updata_m():
    client = MongoClient(host='192.168.1.51')
    db = client['pltaobao']
    collection = db['tb_anchor']
    collection1 = db['tb_anchor1']
    for i in collection.find({}):
        data = {
            "accountId": i['accountId'],
            "accountName": i['accountName'],
            'fansNum': int(i['fansNum']),
            'headImg_url': i['headImg_url'],
            "alliveId": int(i['alliveId']),
            "allpv": int(i['allpv']),
            'alluv': int(i['alluv']),
            'countitemId': int(i['countitemId']),
            "countshopId": int(i['countshopId']),
            "evepv": int(i['evepv']),
            'eveuv': int(i['eveuv']),
            'liveId': i['liveId'],
            'evetaobaoclass2scale': i['evetaobaoclass2scale'],
            'create_time': i['create_time']
        }
        collection1.insert_one(data)


if __name__ == '__main__':
    updata_m()