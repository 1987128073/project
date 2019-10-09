import json

import redis
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.exceptions import PocoNoSuchNodeException
from config import environments
from pymongo import MongoClient
from utils.sign import send_sign
from utils.wirte_logs import Logger


def init_poco(device_id):
    # auto_setup(__file__, ['Android://127.0.0.1:5037/43b5f15d'])
    auto_setup(__file__, [f'Android://127.0.0.1:5037/{device_id}'])
    poco = AndroidUiautomationPoco()
    return poco


def init_app():
    stop_app('com.taobao.live')
    start_app('com.taobao.live')


def init_all(device_id):
    poco = init_poco(device_id)
    init_app()
    time.sleep(3)
    try:
        poco('android:id/button2').click()  # 取消更新
    except PocoNoSuchNodeException:
        pass
    poco("com.taobao.live:id/homepage2_search_btn").click()
    return poco


def search(poco, anchor_name, device_id):
    try:
        poco("com.taobao.live:id/taolive_search_edit_text").set_text(anchor_name)
        poco("com.taobao.live:id/taolive_search_button").click()
    except PocoNoSuchNodeException:
        poco = init_all(device_id)
        search(poco, anchor_name, device_id)


def check_anchor(env_dict, anchorName):
    clent = MongoClient(env_dict.get('mongodb_host'), port=env_dict.get('mongodb_port'))
    db = clent['v3_app_data_parsed']
    res = db['anchors'].find_one({'nick': anchorName})
    if res:
        return res.get('_id')
    else:
        return 0


def run(env, device_id):
    env_dict = environments.get(env)
    r = redis.StrictRedis().from_url(url=env_dict.get('redis_url'))  # 线上或测试redis
    r_2 = redis.StrictRedis(host='192.168.1.180', port=30378)  # 任务redis

    while 1:
        result = r.spop('anchorName:RoomId:uid')

        if result:
            result = result.decode('utf-8').replace('"', '')

            try:
                # 任务数据解析出来有可能不符合预料值
                anchorName = result.split(':')[0]
                roomId = result.split(':')[1]
                uid = result.split(':')[2]
            except:
                continue

            # 查看redis中有没有该用户的缓存
            rs = r_2.get(f'anchor_name:{anchorName}')

            if rs:
                flag = rs.decode('utf-8')
                if flag == '1':  # 30分钟之内1正在爬的用户
                    send_sign(uid, env, anchorName, roomId, num=1)
                    Logger('logs/check_anchor.log', level='info').logger.info(f'{anchorName}:{rs.decode("utf-8")}：该主播正在爬')
                    # print(f'{anchorName}:{rs.decode("utf-8")}：该主播正在爬')
                else:  # 没有该主播
                    send_sign(uid, env, anchorName, roomId, num=3)
                    Logger('logs/check_anchor.log', level='info').logger.info(f'{anchorName}:{rs.decode("utf-8")}：没有该主播')
                    # print(f'{anchorName}:{rs.decode("utf-8")}：没有该主播')
                continue

            anchor_id = check_anchor(env_dict, anchorName)  # 缓存中没有数据，择去数据库中查找该用户
            if anchor_id:  # 若有该用户则直接push任务
                v = {
                    'type': 'operate_broadcaster',
                    'id': anchor_id
                }

                r_2.lpush('operate_broadcaster:tasks', json.dumps(v))
                Logger('logs/check_anchor.log', level='info').logger.info(f'(search_anchor.py)已找到该主播:{anchorName},任务推送成功！')
                continue

            poco = init_all(device_id)
            search(poco, anchorName, device_id)  # 手淘直播查询用户
            time.sleep(5)
            r.sadd('anchorName:RoomId:uid:app', f'{anchorName}:{roomId}:{uid}:app')  # push任务


if __name__ == '__main__':
    import sys

    device_id = sys.argv[1]
    env_name = sys.argv[2]

    run(env_name, device_id)
