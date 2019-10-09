import redis
import requests
from pymongo import MongoClient

from config import environments


class AnchorInfo(object):

    def __init__(self, env):
        self.url = 'https://web.zhiboshuju.com/shopanchorWeChat/selectanchotName'
        self.user = '6c5dbbd2ca3711e9a636a4dcbe0b590c'
        self.openId = 'ofYto04ZtE57zTesjffxdeWmZzQQ'

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'Referer': 'https://web.zhiboshuju.com/shuju/showDataweb?tapType=anchorTap&openId=&userId=6c5dbbd2ca3711e9a636a4dcbe0b590c',
        }

        self.env_dict = environments.get(env)
        self.r = redis.StrictRedis().from_url(url=self.env_dict.get('redis_url'))
        self.clent = MongoClient(self.env_dict.get('mongodb_host'), port=self.env_dict.get('mongodb_port'))
        self.db = self.clent['pltaobao']

    def save_data(self, id, name, anchorPhoto):
        self.r.sadd('anchorId', str(id))
        self.r.sadd('anchorName', name)
        collection = self.db['anchor_info']
        res = collection.find_one({'anchorId': str(id)})
        if not res:
            data = {

                'anchorId': str(id),
                'anchorName': name,
                'houseId': None,
                'fansCount': None,
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
            collection.insert_one(data)

    def get_data(self, anchor_name):

        data = {
            'user': self.user,
            'accountName': anchor_name,
        }

        rs = requests.post(url=self.url, data=data, headers=self.headers,).json()
        if rs.get('cnMessage') == '成功':
            anchor_list = rs.get('data')
            if anchor_list:
                for data in anchor_list:
                    id = data.get('accountId')
                    nickname = data.get('accountName')
                    anchorPhoto = data.get('headImg')
                    # print(id, nickname,)
                    if nickname == anchor_name:
                        anchorId = id
                        self.save_data(id, nickname, anchorPhoto)
                        break
                    else:
                        anchorId = None
                        self.save_data(id, nickname, anchorPhoto)
            else:
                anchorId = None
        else:
            anchorId = None
        # print(anchorId)
        return anchorId


if __name__ == '__main__':
    ai = AnchorInfo('dev')
    ai.get_data('大大超美肤馆')