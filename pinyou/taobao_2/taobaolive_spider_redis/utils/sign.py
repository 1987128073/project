import requests

from config import environments
from utils.wirte_logs import Logger


def send_sign(uid, env, anchorName, roomId, num):
    env_dict = environments.get(env)

    '''
    :param uid: 回调uid
    :param env: 环境
    :param anchorName:
    :param roomId:
    :return:
    '''

    try:
        uid = int(uid)
        requests.post(url=env_dict.get('callback_url'),
                      data={"uid": int(uid), 'anchorState': num, 'anchorName': anchorName, 'roomId': roomId})
    except Exception as e:
        Logger('check_anchor.log', level=env_dict.get('log_type')).logger.info(f'{e}')
        requests.post(url=env_dict.get('callback_url'),
                      data={"uid": 0, 'anchorState': 3, 'anchorName': anchorName, 'roomId': roomId})