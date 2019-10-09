import hashlib
import json
import time

import redis
import requests
from pymongo import MongoClient

from config import environments


class AnchorInfo(object):

    def __init__(self, env):
        self.timestamp = int(time.time()*1000)
        self.token = '5150b38f29904b4836a21c355189a43ae0a873b31c7881232a4f4730d1bc344d'
        self.url = 'https://do.comfire.cn/caihui/anchor/getAnchorInfoForNickName'
        self.headers = {
                    'Content-Type': 'application/json;charset=UTF-8', 'ETag': '1387aa53', 'Referer': 'https://www.hh1024.com/',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
                }

        self.env_dict = environments.get(env)
        self.r = redis.StrictRedis().from_url(url=self.env_dict.get('redis_url'))
        self.clent = MongoClient(self.env_dict.get('mongodb_host'), port=self.env_dict.get('mongodb_port'))
        self.db = self.clent['pltaobao']

    def data_sha256(self, param):
        s = 'param' + str(param) + '&timestamp=' + str(self.timestamp) + '&tenant=caihui&token=' + self.token
        sha = hashlib.sha256()
        sha.update(s.encode())
        sign = sha.hexdigest()
        return sign

    def save_data(self, id, name, fansCount, anchorPhoto):
        self.r.sadd('anchorId', str(id))
        self.r.sadd('anchorName', name)
        collection = self.db['anchor_info']
        res = collection.find_one({'anchorId': str(id)})
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
            collection.insert_one(data)  # 插入一条不存在的主播数据

    def get_anchor_info(self, name):


        param = {
            "anchorEntry": {"searchWord": name},
            "pageEntry": {"pageSize": 10, "pageNum": 1, "sortBy": 1}
        }
        params = {
            "tenant": "caihui",
            "timestamp": self.timestamp,
            "token": self.token,
            "sign": self.data_sha256(param),
            "param": param
        }
        response = requests.post(url=self.url, headers=self.headers, data=json.dumps(params)).json().get('preload').get(
            'results')
        # print(response)
        if response:
            for data in response:
                id = data.get('anchorId')
                nickname = data.get('anchorName')
                fansCount = data.get('fansNum')
                anchorPhoto = data.get('picUrl')
                # print(id, nickname)
                if nickname == name:
                    anchorId = id
                    self.save_data(id, nickname, fansCount, anchorPhoto)
                    break
                else:
                    anchorId = None
                    self.save_data(id, nickname, fansCount, anchorPhoto)
        else:
            anchorId = None
        # print(anchorId)
        return anchorId


if __name__ == '__main__':
    ai = AnchorInfo('dev')
    ai.get_anchor_info('大大超美肤馆')