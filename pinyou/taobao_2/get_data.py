import csv
import os

import redis
from lxml import etree

def get_data():
    for name in os.listdir('./html'):
        list = []
        with open('shop.csv', 'a', encoding='utf-8', newline='') as f:
            writer = csv.writer(f, dialect='excel')
            with open(name, 'r', encoding='utf-8') as f:
                html = etree.HTML(f.read())
                user_url_list = html.xpath(
                    '//*[@id="ice_container"]/div/div/div[2]/div/div[1]/div[4]/div/div/div[1]/div[1]/div/a/@href')
                username = html.xpath(
                    '//*[@id="ice_container"]/div/div/div[2]/div/div[1]/div[4]/div/div/div[1]/div[1]/div/a/div[3]/h3/text()')
                fanscount = html.xpath(
                    '//*[@id="ice_container"]/div/div/div[2]/div/div[1]/div[4]/div/div/div[1]/div[1]/div/a/div[3]/div[1]/span[2]')
                for a,b,c in zip(user_url_list, username, fanscount):

                    list.append(list(a,b,c))
                for d in list:
                    push_user(d[0])
                    writer.writerow(d)


def push_user(user):
    r=redis.StrictRedis(host='192.168.1.45', port=6379, db=0, password='admin')
    r.sadd('goods_category_set', user)
    print('成功')