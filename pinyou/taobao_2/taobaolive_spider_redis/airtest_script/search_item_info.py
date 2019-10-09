import redis
from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.exceptions import PocoNoSuchNodeException
from config import environments
from pymongo import MongoClient


def init_poco(device_id):

    auto_setup(__file__, [f'Android://127.0.0.1:5037/{device_id}'])
    # auto_setup(__file__, ['Android:///'])
    poco = AndroidUiautomationPoco()
    return poco


def init_app(app_name):
    stop_app(app_name)
    start_app(app_name)


def init_all(device_id, app_name):
    poco = init_poco(device_id)
    init_app(app_name)
    time.sleep(2)
    return poco


def get_item_info(poco, item_id):
    try:
        poco("com.fgjkh.tuysas:id/f2").click()
        poco("com.fgjkh.tuysas:id/at").set_text(f'https://h5.m.taobao.com/awp/core/detail.htm?ft=t&id={item_id}')
        keyevent("ENTER")
        time.sleep(6)
        if poco('btn-submit').exists():
            poco("username").set_text('13167617973')
            poco("password").set_text('zc123456789')
            poco("btn-submit").click()
            # time.sleep(5)
            # poco("com.fgjkh.tuysas:id/at").click()
    except PocoNoSuchNodeException:
        pass


if __name__ == '__main__':
    env_dict = environments.get('dev')
    r = redis.StrictRedis().from_url(url=env_dict.get('redis_url'))
    # r_2 = redis.StrictRedis(host='192.168.1.180', port=30378)
    device_id = '63af999e'
    app_name = 'com.fgjkh.tuysas'
    poco = init_all(device_id, app_name)

    while 1:
        result = r.spop('item_id')

        if result:
            item_id = result.decode('utf-8').replace('"', '')
            get_item_info(poco, item_id)
            time.sleep(5)

