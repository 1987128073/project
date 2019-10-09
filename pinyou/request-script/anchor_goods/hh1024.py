from anchor_goods.hh1024task import Aid
import threading
from anchor_goods.hh1024tb_anchor_good import get_sellCount

aid = Aid()
threads = []
t1 = threading.Thread(target=aid.get_liveid)
threads.append(t1)
t2 = threading.Thread(target=aid.get_goods_data)
threads.append(t2)
t3 = threading.Thread(target=get_sellCount)
threads.append(t3)


if __name__ == '__main__':
    for t in threads:
        t.start()
    for t in threads:
        t.join()
