import redis

def conn_redis(redis_url):
    r = redis.StrictRedis().from_url(url=redis_url)
    return r