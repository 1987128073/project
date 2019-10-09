# -*- coding: utf-8 -*-
import redis

r = redis.StrictRedis(host='192.168.1.45', port=6379, db=0, password='admin')
l = ['家庭/个人清洁工具','生活电器','饰品/流行首饰/时尚饰品新','彩妆/香水/美妆工具','美发护发/假发','奶粉/辅食/营养品/零食','咖啡/麦片/冲饮','零食/坚果/特产','孕妇装/孕产妇用品/营养','女士内衣/男士内衣/家居服','女鞋','女装/女士精品','服饰配件/皮带/帽子/围巾','箱包皮具/热销女包/男包']

def redis_data_set_to_list():
    while 1:
        if not r.llen('tbspider:start_urls'):
            try:
                w = l.pop()
                # r.lpush('tbspider:start_urls', w)
                r.lpush('tbsearchspider:start_urls', w)
            except:
                break



def redis_lpush():

    # r.lpush('tbspider:start_urls', '美发护发/假发')
    r.lpush('tbsearchspider:start_urls', '家庭/个人清洁工具')
    print('添加成功')



if __name__ == '__main__':
    # redis_lpush()
    redis_data_set_to_list()