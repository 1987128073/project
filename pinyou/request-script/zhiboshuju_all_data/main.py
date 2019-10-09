import threading
from zhuboshuju_goods_spider import GoodsSpider
from zhuboshuju_dianshangji import DianShangJi

env = 'dev'
dsj = DianShangJi(env)
gs = GoodsSpider(env)
threads = []

t2 = threading.Thread(target=dsj.get_sellCount)
threads.append(t2)
t3 = threading.Thread(target=gs.get_data)
threads.append(t3)


if __name__ == '__main__':
    for t in threads:
        t.start()

