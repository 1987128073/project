import json
import time

import redis
import requests
from pymongo import MongoClient
from requests.auth import HTTPProxyAuth
r = redis.StrictRedis(host='192.168.1.45', port=6379, db=0, password='admin')
client = MongoClient('192.168.1.45')
db1 = client['test']
db2 = client['pltaobao']
collection = db2['tb_anchor_goods']

def get_sellCount():

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',

    }
    proxies = {
                'http': 'http://http-proxy-t1.dobel.cn:9180'
            }

    auth = HTTPProxyAuth('ATLANDG4EGPK5S0', 'LKHN5uFx')
    num = 0
    while 1:
        count = 1000
        all_data = collection.find().skip(count*num).limit(1000)
        num += 1
        for data in all_data:

            if not check_task('{}:{}'.format(data.get('accountId'), data.get('itemId'))):
                continue
            json_obj = requests.get(url='https://acs.m.taobao.com/gw/mtop.taobao.detail.getdetail/6.0/?data=%7B"itemNumId"%3A"{}"%7D'.format(data.get('itemId')), headers=headers,proxies=proxies, auth=auth).json()
            if json_obj.get('data') and json_obj.get('data').get('apiStack'):
                try:
                    value = json_obj.get('data').get('apiStack')[0].get('value')
                except:
                    value = None
                    FailGetLiveData(data.get('itemId'))
                if value:
                    item = json.loads(value).get('item')
                    if item:
                        try:
                            sellcount = item.get('sellCount')
                        except:
                            sellcount = item.get('vagueSellCount')
                        if not sellcount:
                            sellcount = 0
                        print(data.get('accountId'), sellcount, '-------', num)
                        collection.update_one({'accountId': data.get('accountId'), 'itemId': data.get('itemId')}, {'$set': {'SellCount': sellcount}})
            time.sleep(5)

def check_task(taskname):
    res = db1['tb_anchor_goods_Task'].find_one({'_id': str(taskname)})
    if not res:
        db1['tb_anchor_goods_Task'].insert_one({'_id': str(taskname)})
        return 1
    else:
        return 0

def FailGetLiveData(id):
    r.sadd('FailToGetItemSellCount', id)


if __name__ == '__main__':
    get_sellCount()