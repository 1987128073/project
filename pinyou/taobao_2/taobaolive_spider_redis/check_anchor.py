import json
import time

import redis
from pymongo import MongoClient
from config import environments
from search_anchor_info.hh1024_get_anchorInfo import AnchorInfo as AI_hh1024
from search_anchor_info.zhiboshuju_get_anchor_info import AnchorInfo as AI_zhiboshuju
from utils.sign import send_sign
from utils.wirte_logs import Logger


def check_anchor(env):
    '''
    通过本地数据库和第三方网站检测主播是否存在
    :param env:
    :return:
    '''
    env_dict = environments.get(env)
    r = redis.StrictRedis().from_url(url=env_dict.get('redis_url'))
    r_2 = redis.StrictRedis(host='192.168.1.180', port=30378)
    clent = MongoClient(env_dict.get('mongodb_host'), port=env_dict.get('mongodb_port'))
    db = clent['v3_app_data_parsed']
    while 1:
        result = r.spop('anchorName:RoomId:uid:app')

        if result:

            result = result.decode('utf-8').replace('"', '')

            # 任务数据解析出来有可能不符合预料值
            anchorName = result.split(':')[0]
            roomId = result.split(':')[1]
            uid = result.split(':')[2]

            try:

                res = db['anchors'].find_one({'nick': anchorName})
                if not res:
                    res = {}
                    anchor_info = AI_hh1024(env)
                    id = anchor_info.get_anchor_info(anchorName)
                    if id:
                        res['anchorId'] = id
                    else:
                        anchor_info = AI_zhiboshuju(env)
                        res['anchorId'] = anchor_info.get_data(anchorName)

            except Exception as e:
                Logger('logs/check_anchor.log', level='info').logger.error(f'{e}')
                send_sign(uid, env, anchorName, roomId, num=3)
                continue

            if res.get('anchorId'):
                anchorId = res.get('anchorId')

                v = {
                    'type': 'operate_broadcaster',
                    'id': anchorId
                }

                r_2.lpush('operate_broadcaster:tasks', json.dumps(v))
                r.sadd('schedule_task:anchorId', anchorId)
                send_sign(uid, env, anchorName, roomId, num=1)
                # r.sadd('anchorId:anchorName:uid:roomId:env', f'{anchorId}:{anchorName}:{uid}:{roomId}:{env}')
                Logger('logs/check_anchor.log', level='info').logger.info(f'(check_anchor.py)已找到该主播:{anchorName},任务推送成功！')
                # print(f'已找到该主播:{anchorName}')
                r_2.set(f'anchor_name:{anchorName}', 1, 1800)
                save_task_schedule(anchorName, anchorId, clent)
            else:
                send_sign(uid, env, anchorName, roomId, num=3)
                Logger('logs/check_anchor.log', level='info').logger.info(f'(check_anchor.py)未找到该主播:{anchorName},任务推送失败！')
                # print(f'未找到该主播:{anchorName}')
                r_2.set(f'anchor_name:{anchorName}', 0, 1800)


def save_task_schedule(anchorName, anchorId, clent):
    db = clent['v3_monitoring']
    res = db['anchors'].find_one({'_id': anchorId})
    if not res:
        data = {
            '_id': int(anchorId),
            'name': anchorName,
            'create_time': int(time.time()),
            'update_time': int(time.time()),
            'state': True,

        }
        db['anchors'].insert_one(data)
        Logger('logs/check_anchor.log', level='info').logger.info(f'(check_anchor.py){anchorName},已推送到调度表！')


if __name__ == '__main__':
    import sys
    env_name = sys.argv[1]
    check_anchor(env_name)
