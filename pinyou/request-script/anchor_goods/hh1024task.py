# -*- coding: utf-8 -*-
import hashlib
import json
import logging
import time
import redis
import requests
from pymongo import MongoClient


class Aid(object):

    def __init__(self):
        self.num = 0
        self.url = 'https://do.comfire.cn/caihui/anchor/getAnchorInfoForNickName'
        self.liveId_url = 'https://do.comfire.cn/caihui/anchor/getAnchorHistoryInfo'
        self.goods_list_url = 'https://do.comfire.cn/caihui/liveInfo/getGoodsList'
        self.r = redis.StrictRedis(host='192.168.1.45', port=6379, db=1, password='admin')
        self.headers = {
            'Content-Type': 'application/json;charset=UTF-8', 'ETag': '1387aa53', 'Referer': 'https://www.hh1024.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }
        self.timestamp = int(time.time()*1000)
        self.token = '5150b38f29904b4836a21c355189a43ae0a873b31c7881232a4f4730d1bc344d'  # 登录用户唯一token，可能在一段时间后会改变
        self.mongo_port = 32766
        self.db = MongoClient('192.168.1.45')['test']
        self.collection = self.db['anchor_info']

    def get_data(self):
        words = self.r.smembers('AnchorNickname')
        for word in words:
            self.num += 1
            print(self.num)
            param = {
                "anchorEntry": {"searchWord": str(word.decode('utf-8'))},
                "pageEntry": {"pageSize": 100, "pageNum": 1, "sortBy": 1}
            }
            params = {
                "tenant": "caihui",
                "timestamp": self.timestamp,
                "token": self.token,
                "sign": self.data_sha256(param),
                "param": param
            }
            response = requests.post(url=self.url, headers=self.headers, data=json.dumps(params)).json().get('preload').get('results')
            # print(response)
            if response:
                for index in response:
                    id = index.get('anchorId')
                    nickname = index.get('anchorName')
                    fansCount = index.get('fansNum')
                    anchorPhoto = index.get('picUrl')
                    if id:
                        self.save_data(id, nickname, fansCount, anchorPhoto)
                    else:
                        continue

    def get_liveid(self):
        while 1:
            id = self.r.spop('anchorId_pop')
            if not id:
                time.sleep(10)
            else:
                param = {
                    "anchorLiveHistoryEntry": {"anchorId": str(id.decode('utf-8')), "days": 30}
                }
                params = {
                    "tenant": "caihui",
                    "timestamp": self.timestamp,
                    "token": self.token,
                    "sign": self.data_sha256(param),
                    "param": param
                }
                response = requests.post(url=self.liveId_url, headers=self.headers, data=json.dumps(params)).json().get('preload')
                if response.get('result') and response.get('result').get('liveScene'):
                    response = response.get('result')
                    self.save_liveid(str(id.decode('utf-8')), response.get('liveIdList'))

    def save_liveid(self, anchorId, livelist):
        for a in livelist:
            self.r.sadd('liveId', a)
            res = self.db['Id_of_live_broadcast_of_anchor'].find_one({'_id': anchorId, 'LiveId': a})
            if not res:
                data = {
                    '_id': str(anchorId),
                    'LiveId': a,
                }
                self.db['Id_of_live_broadcast_of_anchor'].insert_one(data)

    def get_goods_data(self):
        while 1:
            liveid = self.r.spop('liveId')
            if not liveid:
                time.sleep(5)
            else:
                param = {
                    "itemEntry": {"liveIdList": [liveid.decode('utf-8')]},
                    "pageEntry": {"pageNum": 1, "pageSize": 500, "sortBy": 1}
                }
                params = {
                    "tenant": "caihui",
                    "timestamp": self.timestamp,
                    "token": self.token,
                    "sign": self.data_sha256(param),
                    "param": param
                }
                response = requests.post(url=self.goods_list_url, headers=self.headers, data=json.dumps(params)).json()
                # print(response)
                if response.get('preload') and response.get('preload').get('results'):
                    liveid = liveid.decode('utf-8')
                    liveid_goods = response.get('preload').get('results')
                    self.save_liveid_goods(liveid, liveid_goods)
                else:
                    self.FailGetLiveData(liveid.decode('utf-8'))
                time.sleep(1.5)

    def save_data(self, id, name, fansCount, anchorPhoto):
        self.r.sadd('anchorId', str(id))
        self.r.sadd('anchorName', name)
        res = self.collection.find_one({'anchorId': str(id)})
        if not res:
            data = {

                'anchorId': str(id),
                'anchorName': name,
                'houseId': None,
                'fansCount': int(fansCount),
                'liveCount': None,
                'city': None,
                'creatorType': None,
                'darenScore': None,
                'descText': None,
                'anchorPhoto': anchorPhoto,
                'organId': None,
                'fansFeature': None,
                'historyData': None,
            }
            self.collection.insert_one(data)  # 插入一条不存在的主播数据
        # else:
        #     if res.get('fansCount') == int(fansCount) and res.get('anchorPhoto') == anchorPhoto:
        #         pass
        #     else:
        #         self.collection.update_one({'anchorId': str(id)}, {'$set': {'fansCount': fansCount, 'anchorPhoto': anchorPhoto}})  # 更新已存在的主播数据

    def data_sha256(self, param):
        s = 'param'+str(param)+'&timestamp='+str(self.timestamp)+'&tenant=caihui&token='+self.token
        sha = hashlib.sha256()
        sha.update(s.encode())
        sign = sha.hexdigest()
        return sign

    def save_liveid_goods(self, liveid, result):
        for s in result:
            self.r.sadd('itemid', s.get('itemId'))
            res_list = self.db['Id_of_live_broadcast_of_anchor'].find({'LiveId': liveid})

            response = self.db['LiveData'].find_one({'LiveId': str(liveid), 'itemId': str(s.get('itemId'))})
            if not response:
                data = {
                    'anchorId': res_list.get('_id'),
                    'LiveId': str(liveid),
                    'itemId': str(s.get('itemId')),
                    'liveGoodsData': s
                }
                self.db['LiveData'].insert_one(data)

    def FailGetLiveData(self, id):
        self.r.sadd('FailToGetLiveData', id)

    def run(self):
        # self.get_data()
        # self.get_liveid()
        self.get_goods_data()


class CopySet(object):

    def __init__(self, host='192.168.1.45', port=6379, password=None):
        self.host = host
        self.port = port
        self.password = password
        self.r = redis.StrictRedis(host=self.host, port=self.port, db=0, password=self.password)

    def __copy__(self):
        if self.r.type(self.oldkey).decode('utf-8') != 'set':
            raise logging.error('不是set类型数据')
        values = self.r.smembers(self.oldkey)
        if not values:
            raise logging.error('oldkey不存在')
        if self.r.smembers(self.newkey):
            raise logging.error('newkey已存在')

        for value in values:
            self.r.sadd(self.newkey, value)
        return logging.info('成功')

    def run(self,oldkey,newkey):
        self.oldkey = oldkey
        self.newkey = newkey
        self.__copy__()



if __name__ == '__main__':

    # copyset = CopySet(password='admin')
    # copyset.run('anchorId', 'anchorId_pop')
    aid = Aid()
    aid.get_liveid()
    # aid.test_get_goods_data()