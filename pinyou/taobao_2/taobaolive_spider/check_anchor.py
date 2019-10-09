import redis
from pymongo import MongoClient
from config import environments
from hh1024.hh1024_get_anchorInfo import AnchorInfo
from send_msg import push_task
from utils.sign import send_sign
from utils.wirte_logs import Logger


def check_anchor(env):
    '''
    通过本地数据库和第三方网站检测主播是否存在
    :param env:
    :return:
    '''
    env_dict = environments.get(env)
    r = redis.StrictRedis().from_url(url=env_dict.get('redis_url'))
    clent = MongoClient(env_dict.get('mongodb_host'), port=env_dict.get('mongodb_port'))
    db = clent['pltaobao']
    while 1:
        result = r.spop('anchorName:RoomId:uid')
        if result:

            result = result.decode('utf-8').replace('"', '')

            # 任务数据解析出来有可能不符合预料值
            anchorName = result.split(':')[0]
            roomId = result.split(':')[1]
            uid = result.split(':')[2]

            try:

                res = db['anchor_info'].find_one({'anchorName': anchorName})
                print(anchorName)
                if not res:
                    res = {}
                    anchor_info = AnchorInfo(env)
                    id = anchor_info.get_anchor_info(anchorName)
                    if id:
                        res['anchorId'] = id
            except Exception as e:
                Logger('check_anchor.log', level='info').logger.error(f'{e}')
                send_sign(uid, env, anchorName, roomId, num=3)
                continue

            if res:
                anchorId = res.get('anchorId')
                if env == 'dev':
                    push_task('anchorId:anchorName:uid:roomId', 'anchorId:anchorName:uid:roomId',
                              f'{anchorId}:{anchorName}:{uid}:{roomId}')
                elif env == 'pro':
                    push_task('anchorId:anchorName:uid:roomId:env', 'anchorId:anchorName:uid:roomId:env', f'{anchorId}:{anchorName}:{uid}:{roomId}:{env}', env)


if __name__ == '__main__':
    check_anchor('dev')
