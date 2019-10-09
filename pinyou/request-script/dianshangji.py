import csv
import datetime
import time

import redis
from pymongo import MongoClient
from selenium import webdriver as wb

from tool_.time_change import timestamp_to_timestr


class DianShangJi(object):

    def __init__(self):
        self.clent = MongoClient('192.168.1.45')
        self.db = self.clent['pltaobao']
        self.collection = self.db['tb_anchor_goods']
        self.r = redis.StrictRedis(host='192.168.1.45')
        self.browser = wb.Edge()
        self.base_url = 'https://m.dianshangji.com/analyst_mtaobaodaydb/analyst.html?itemid={}#itemid={}'

    def get_sellCount(self):
        with open(r'C:\Users\Admin\PycharmProjects\pinyou\request-script\file\{}.csv'.format('engeeritems'), 'r',
                  encoding='utf-8') as f:
            csv_data = csv.reader(f, dialect='excel')
            for data in csv_data:
                with open(r'C:\Users\Admin\PycharmProjects\pinyou\request-script\file\{}.csv'.format('time'), 'r',
                  encoding='utf-8') as f:
                    csv_data2 = csv.reader(f, dialect='excel')
                    for i in csv_data2:
                        if i[0] == data[2]:
                            start_time = i[7]

                            time_str = timestamp_to_timestr(int(start_time)/1000)
                            itemId = data[1]
                            self.browser.get(self.base_url.format(itemId, itemId))
                            time.sleep(8)
                            html_data = self.browser.find_elements_by_xpath('//table[@id="metrictable"]/tbody/tr')
                            flag = 0
                            for a in html_data:
                                if a.text[:10] == time_str[:10]:
                                    flag = 1
                                    l = a.text.split(' ')
                                    print(l)
                                    Monthly_payment = int(l[2].split('\n')[0])
                                    try:
                                        CommtentCount = int(l[2].split('\n')[-2].replace('(', '').replace(')', ''))
                                    except:
                                        CommtentCount = 0

                                    self.insert_data(data, Monthly_payment, CommtentCount, time_str)
                                    break
                            if flag == 0:
                                self.insert_data(data, 0, 0, time_str)

    def insert_data(self, data, Monthly_payment, CommtentCount,time_str):
        res = self.db[f'{data[3]}'].find_one({'_id': data[0]})
        if not res:
            dict = {
                '_id': data[0],
                'product_id': data[1],
                'live_id': data[2],
                'anchor_id': data[3],
                'start_time': time_str,
                'Monthly_payment': Monthly_payment,
                'CommtentCount': CommtentCount
            }

            self.db[f'{data[3]}'].insert_one(dict)


    def get_url(self):
        while 1:
            id = self.r.spop('dianshangji_itemId')
            if not id:
                time.sleep(5)
                print('暂无任务，请添加')
            else:
                self.browser.get(self.base_url.format(id.decode('utf-8'), id.decode('utf-8')))
                time.sleep(5)
                data = self.browser.find_elements_by_xpath('//table[@id="metrictable"]/tbody/tr')
                data_list = []
                for index, a in enumerate(data):
                    item = {}
                    if index != 0:
                        l = a.text.split(' ')
                        item['Time_str'] = datetime.datetime.strptime(l[0], '%Y-%m-%d')
                        item['Price'] = l[1]
                        item['Monthly_payment'] = float(l[2].split('\n')[0])
                        item['CommtentCount'] = int(l[2].split('\n')[-1])
                        data_list.append(item)
                self.save(id.decode('utf-8'), data_list)

    def save(self, id, data_list):
        res = self.collection.find_one({'_id': str(id)})
        if not res:
            data = {
                '_id': str(id),
                'goodsinfo': data_list,
            }
            self.collection.insert_one(data)
        else:

            pass

    def check_task(self, taskname):
        res = self.clent['Task']['dianshangjiTask'].find_one({'_id': str(taskname)})
        if not res:
            self.clent['Task']['dianshangjiTask'].insert_one({'_id': str(taskname)})
            return 1
        else:
            return 0

    def __close(self):
        # self.browser.quit()
        pass

    def push_itemid_to_redis(self):
        data = self.collection.find()
        for d in data:
            self.r.sadd('itemId', d.get(''))

    def run(self):
        # self.get_url()
        self.get_sellCount()
        self.__close()


if __name__ == '__main__':
    dsj = DianShangJi()
    dsj.run()