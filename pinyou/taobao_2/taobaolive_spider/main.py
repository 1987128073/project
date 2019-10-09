import threading

from Mitm_get_anchor_info import get_anchor_info
from Mitm_get_live_info import get_live_info
from check_anchor import check_anchor
from parse_livedetail import ParseData
from receive_msg import ConsumingMsg

env = 'pro'
if env == 'pro':
    pd = ParseData(env)
    cm = ConsumingMsg(queue_name='anchorId:anchorName:uid:roomId:env', env=env, func=get_anchor_info)
    cm2 = ConsumingMsg(queue_name='anchorId:liveId:pro', env=env, func=get_live_info)
else:
    pd = ParseData(env)
    cm = ConsumingMsg(queue_name='anchorId:anchorName:uid:roomId', env=env, func=get_anchor_info)
    cm2 = ConsumingMsg(queue_name='anchorId:liveId', env=env, func=get_live_info)

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

t5 = threading.Thread(target=cm.consuming_task)
threads.append(t5)

t7 = threading.Thread(target=cm2.consuming_task)
threads.append(t7)


if __name__ == '__main__':
    for t in threads:
        t.start()

