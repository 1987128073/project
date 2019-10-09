from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from poco.exceptions import PocoNoSuchNodeException


def init_poco():
    auto_setup(__file__, ['Android:///'])
    poco = AndroidUiautomationPoco()
    return poco


def init_app():
    stop_app('com.taobao.live')
    start_app('com.taobao.live')


def init_all():
    poco = init_poco()
    init_app()
    time.sleep(5)
    try:
        poco('android:id/button2').click()  # 取消更新
    except PocoNoSuchNodeException:
        pass
    return poco


def search(poco, anchor_name):

    poco("com.taobao.live:id/homepage2_search_btn").click()
    poco("com.taobao.live:id/taolive_search_edit_text").set_text(anchor_name)
    poco("com.taobao.live:id/taolive_search_button").click()


if __name__ == '__main__':
    poco = init_all()
    search(poco, '雯雯PL哒')