import threading

from Mitm_get_anchor_info import get_anchor_info
from Mitm_get_live_info import get_live_info
from check_anchor import check_anchor
from parse_data import ParseData


env = 'dev'
pd = ParseData(env)

threads = []

# pares_itemlist function
t1 = threading.Thread(target=pd.parse_itemlist)
threads.append(t1)
# pares_livedetail function
t2 = threading.Thread(target=pd.parse_livedetail)
threads.append(t2)
# pares_feedsdetail function
t3 = threading.Thread(target=pd.parse_feedsdetail)
threads.append(t3)
# check_anchor function
t4 = threading.Thread(target=check_anchor, args=(env,))
threads.append(t4)

t5 = threading.Thread(target=get_anchor_info, args=(env,))
threads.append(t5)

t7 = threading.Thread(target=get_live_info, args=(env,))
threads.append(t7)


if __name__ == '__main__':
    for t in threads:
        t.start()

