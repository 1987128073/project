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


def get_item_info(poco):

    poco("android.widget.LinearLayout").offspring("com.taobao.live4anchor:id/tab").child(
        "android.widget.LinearLayout").child("android.support.v7.app.ActionBar$Tab")[2].click()

    time.sleep(8)

    poco("找达人").click()
    time.sleep(5)

    poco("筛选").click()

    poco(text="淘宝直播").click()
    poco("android.widget.LinearLayout").offspring("com.taobao.live4anchor:id/filter_recycler").child(
        "android.widget.LinearLayout")[1].child("com.taobao.live4anchor:id/filter_item").child(
        "com.taobao.live4anchor:id/text")[0].click()

    poco("android.widget.LinearLayout").offspring("com.taobao.live4anchor:id/filter_recycler").child(
        "android.widget.LinearLayout")[2].child("com.taobao.live4anchor:id/filter_item").child(
        "com.taobao.live4anchor:id/text")[0].click()

    poco("android.widget.LinearLayout").offspring("com.taobao.live4anchor:id/filter_recycler").child("android.widget.LinearLayout")[2].child("com.taobao.live4anchor:id/filter_item").child("com.taobao.live4anchor:id/text")[0].swipe([0.0214, -0.3596])

    poco("android.widget.LinearLayout").offspring("com.taobao.live4anchor:id/filter_recycler").child(
        "android.widget.LinearLayout")[2].child("com.taobao.live4anchor:id/filter_item").child(
        "com.taobao.live4anchor:id/text")[0].click()

    poco("com.taobao.live4anchor:id/filter_ok").click()

    while 1:
        poco("com.taobao.live4anchor:id/search_result").swipe([-0.0929, -0.8357])


if __name__ == '__main__':
    device_id = '8dd5b27b'
    app_name = 'com.taobao.live4anchor'
    poco = init_all(device_id, app_name)
    time.sleep(5)
    get_item_info(poco)


