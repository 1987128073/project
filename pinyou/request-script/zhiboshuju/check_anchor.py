import time

import redis
import requests
from pymongo import MongoClient
from config import environments
from hh1024_get_anchorInfo import AnchorInfo
from logs.wirte_logs import Logger


def check_anchor(env):
    '''
    :param env: 配置环境
    :return:
    '''
    env_dict = environments.get(env)
    r = redis.StrictRedis().from_url(url=env_dict.get('redis_url'))
    clent = MongoClient(env_dict.get('mongodb_host'), port=env_dict.get('mongodb_port'))
    db = clent['pltaobao']

    while 1:
        result = r.spop('anchorName:RoomId:uid')
        if result:

            result = result.decode('utf-8').replace('"', '')
            print(result)
            # 任务数据解析出来有可能不符合预料值
            anchorName = result.split(':')[0]
            roomId = result.split(':')[1]
            uid = result.split(':')[2]

            try:

                res = db['anchor_info'].find_one({'anchorName': str(anchorName)})
                print(anchorName, res)
                if not res:
                    res = {}
                    anchor_info = AnchorInfo(env)
                    id = anchor_info.get_anchor_info(anchorName)
                    if id:
                        res['anchorId'] = id

            except Exception as e:
                Logger('check_anchor.log', level='info').logger.error(f'{e}')
                send_sign(uid, env, anchorName, roomId)
                continue

            # 如果没有从数据库中查到主播信息，直接回调，如果有数据则创建任务，丢给爬虫系统爬取信息
            if not res:
                Logger('check_anchor.log', level='info').logger.info(f'未找到该用户：{anchorName}:{roomId}')
                # task = {
                #     "uid": uid,
                #     "anchorName": anchorName,
                #     'roomId': roomId,
                #     'status': 1
                # }
                # r.sadd('senf_sign_task', '{}'.format(task))
                send_sign(uid, env_dict, anchorName, roomId)
                continue
            else:

                anchorId = res.get('anchorId')
                r.sadd('anchorId:anchorName:uid:roomId', f'{anchorId}:{anchorName}:{uid}:{roomId}')
                Logger('check_anchor.log', level=env_dict.get('log_type')).logger.info(
                    f'已找到该用户：{anchorId}:{anchorName}')


def send_sign(uid, env_dict, anchorName, roomId):
    '''
    :param uid: 回调uid
    :param env_dict: 环境
    :param anchorName:
    :param roomId:
    :return:
    '''
    try:
        uid = int(uid)
        requests.post(url=env_dict.get('callback_url'),
                      data={"uid": int(uid), 'anchorState': 3, 'anchorName': anchorName, 'roomId': roomId})
    except Exception as e:
        Logger('check_anchor.log', level=env_dict.get('log_type')).logger.info(f'{e}')
        requests.post(url=env_dict.get('callback_url'),
                      data={"uid": 0, 'anchorState': 3, 'anchorName': anchorName, 'roomId': roomId})


if __name__ == '__main__':
    check_anchor(env='pro')
