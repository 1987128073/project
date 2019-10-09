import json
import pymysql
import redis
import schedule
from pymongo import MongoClient
from utils.wirte_logs import Logger
from config import environments
r_2 = redis.StrictRedis(host='192.168.1.180', port=30378)
env_dict = environments.get('dev')
client = MongoClient(env_dict.get('mongodb_host'), env_dict.get('mongodb_port'))
db = client['v3_monitoring']


def anchor_timing_run():

    res = db['anchors'].find()

    for anchor_info in res:
        anchor_id = anchor_info.get('_id')
        anchor_name = anchor_info.get('name')
        state = anchor_info.get('state')

        if not state:
            continue

        Logger('logs/check_anchor.log', level='info').logger.info(f'(schedele_task.py):{anchor_name}该主播任务推送成功！')

        v = {
            'type': 'operate_broadcaster',
            'id': anchor_id
        }
        r_2.lpush('operate_broadcaster:tasks', json.dumps(v))


def live_timing_run():

    pass


schedule.every(30).minutes.do(anchor_timing_run)

while True:
    schedule.run_pending()
