import redis


def get_category():
    r = redis.StrictRedis(host='192.168.1.45', port=6379, db=0, password='admin')
    a = r.spop('goods_category_set')
    return a

if __name__ == '__main__':
    get_category()