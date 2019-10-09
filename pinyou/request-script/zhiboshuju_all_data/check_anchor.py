import time

import redis
import requests
from pymongo import MongoClient
from config import environments
from wirte_logs import Logger

clent = MongoClient('192.168.1.45')
db = clent['pltaobao']
collection = db['tb_anchor_goods_task']


def check_anchor(env):
    r = redis.StrictRedis().from_url(url=environments.get(env).get('redis_url'))
    while 1:
        result = r.spop('anchorName:RoomId:uid')
        if result:

            result = result.decode('utf-8').replace('"', '')
            res = db['anchor_info'].find_one({'anchorName': result.split(':')[0]})
            if not res:
                send_sign(result.split(':')[2], env)
                continue
            else:
                anchorId = res.get('anchorId')
                r.sadd('anchorId:anchorName:uid', f'{anchorId}:{result.split(":")[0]}:{result.split(":")[2]}')
                Logger('./logs/check_anchor.log', level=environments.get(env).get('log_type')).logger.info(f'{anchorId}:{result.split(":")[0]}')


def send_sign(uid, env):
    try:
        uid = int(uid)
        requests.post(url='http://test.pl298.com:8007/analysis/updateUser', data={"uid": int(uid), 'anchorState': 3})
    except Exception as e:
        Logger('check_anchor.log', level=environments.get(env).get('log_type')).logger.info(f'{e}')
        requests.post(url='http://test.pl298.com:8007/analysis/updateUser', data={"uid": 0, 'anchorState': 3})


if __name__ == '__main__':
    check_anchor(env='pro')