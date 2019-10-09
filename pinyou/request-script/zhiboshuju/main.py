import threading
import asyncio
from zhuboshuju_goods_spider import GoodsSpider
from check_anchor import check_anchor
from zhuboshuju_dsj_selenium import DianShangJi

# import win32api, win32gui
#
# ct = win32api.GetConsoleTitle()
#
# hd = win32gui.FindWindow(0,ct)
#
# win32gui.ShowWindow(hd,0)


env = 'pro'
dsj = DianShangJi(env)
gs = GoodsSpider(env)
threads = []
t1 = threading.Thread(target=check_anchor, args=(env,))
threads.append(t1)
t2 = threading.Thread(target=dsj.get_sellCount2)
threads.append(t2)
t3 = threading.Thread(target=gs.get_data)
threads.append(t3)


if __name__ == '__main__':
    for t in threads:
        t.start()

