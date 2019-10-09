import redis

from config import environments
from wirte_logs import Logger


def push_task(env):
    r = redis.StrictRedis().from_url(url=environments.get(env).get('redis_url'))

    if not r.smembers('anchorId'):
        anchorId_hot = r.smembers('anchorId_hot')
        for i in anchorId_hot:
            r.sadd('anchorId', i.decode('utf-8'))

    else:
        Logger('./logs/timed_task.log', level='info').logger.info(
            '已有key为anchorId！')


if __name__ == '__main__':
    push_task('dev')