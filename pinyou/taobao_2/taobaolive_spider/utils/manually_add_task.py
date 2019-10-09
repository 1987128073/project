import redis

from send_msg import push_task
from taobaolive_spider.config import environments
env_dict = environments.get('test')
r = redis.StrictRedis().from_url(url=env_dict.get('redis_url'))


def add_anchorId_hot_task():
    for i in r.smembers('anchorId_hot'):
        anchorId = i.decode('utf-8')
        push_task('anchorId:anchorName:uid:roomId', 'anchorId:anchorName:uid:roomId', f'{anchorId}:{1}:{1}:{1}')


def add_anchorId_task():
    for i in r.smembers('anchorId_hot'):
        anchorId = i.decode('utf-8')
        push_task('anchorId:anchorName:uid:roomId', 'anchorId:anchorName:uid:roomId', f'{anchorId}:{1}:{1}:{1}')


if __name__ == '__main__':
    add_anchorId_hot_task()