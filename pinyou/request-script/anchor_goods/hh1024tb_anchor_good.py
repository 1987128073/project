import json
import time

import redis
import requests
from pymongo import MongoClient
from requests.auth import HTTPProxyAuth
r = redis.StrictRedis(host='192.168.1.45', port=6379, db=1, password='admin')

def get_sellCount():
    client = MongoClient('192.168.1.45')
    db1 = client['test']
    collection = db1['LiveData']
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',

    }
    proxies = {
                'http': 'http://http-proxy-t1.dobel.cn:9180'
            }

    auth = HTTPProxyAuth('ATLANDG4EGPK5S0', 'LKHN5uFx')
    num = 0
    while 1:
        itemId = r.spop('itemid')
        if not itemId:
            time.sleep(10)
        else:
            time.sleep(6)
            json_obj = requests.get(url='https://acs.m.taobao.com/gw/mtop.taobao.detail.getdetail/6.0/?data=%7B"itemNumId"%3A"{}"%7D'.format(itemId.decode('utf-8')), headers=headers,proxies=proxies, auth=auth).json()
            if json_obj.get('data') and json_obj.get('data').get('apiStack'):
                try:
                    value = json_obj.get('data').get('apiStack')[0].get('value')
                except:
                    value = None
                    FailGetLiveData(itemId.decode('utf-8'))
                if value:
                    item = json.loads(value).get('item')
                    if item:
                        try:
                            sellcount = item.get('sellCount')
                        except:
                            sellcount = item.get('vagueSellCount')
                        if not sellcount:
                            sellcount = 0
                        print(itemId.decode('utf-8'), sellcount, '-------', num)
                        res = collection.find_one({'itemId': itemId.decode('utf-8')})
                        if not res:
                            r.sadd('itemID_dsj', itemId.decode('utf-8'))
                            collection.insert_one({'itemId': itemId.decode('utf-8')}, {'$set': {'SellCount': sellcount}})
                        else:
                            if res.get('SellCount') == sellcount:
                                pass
                            else:
                                collection.update_one({'itemId': itemId.decode('utf-8')},
                                                      {'$set': {'SellCount': sellcount}})


def FailGetLiveData(id):
    r.sadd('FailToGetItemSellCount', id)


if __name__ == '__main__':
    get_sellCount()