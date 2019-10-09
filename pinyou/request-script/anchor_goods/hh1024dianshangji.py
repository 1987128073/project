import datetime
import time

import redis
from pymongo import MongoClient
from selenium import webdriver as wb


class DianShangJi(object):

    def __init__(self):
        self.clent = MongoClient('192.168.1.45')
        self.db = self.clent['pltaobao']
        self.collection = self.db['tb_anchor_goods_task']
        self.r = redis.StrictRedis(host='192.168.1.45')
        self.browser = wb.Edge()
        self.base_url = 'https://m.dianshangji.com/analyst_mtaobaodaydb/analyst.html?itemid={}#itemid={}'


    def get_sellCount(self):
        num = 0
        while 1:
            count = 100
            all_data = self.collection.find().skip(count * num).limit(100)
            num += 1

            for data in all_data:
                itemId = data.get('itemId')
                # if not self.check_task(itemId):
                #     continue

                self.browser.get(self.base_url.format(itemId, itemId))
                time.sleep(8)
                html_data = self.browser.find_elements_by_xpath('//table[@id="metrictable"]/tbody/tr')
                flag = 0
                for a in html_data:
                    if a.text[:10] == data.get('createTime')[:10]:
                        flag = 1
                        l = a.text.split(' ')
                        print(l)
                        Monthly_payment = int(l[2].split('\n')[0])
                        try:
                            CommtentCount = int(l[2].split('\n')[-2].replace('(', '').replace(')', ''))
                        except:
                            break

                        self.collection.update_one({'accountId': str(data.get('accountId')), 'itemId': str(data.get('itemId'))}, {'$set': {'Monthly_payment': Monthly_payment, 'CommtentCount':CommtentCount}})
                        break
                if flag == 0:
                    self.collection.update_one({'accountId': str(data.get('accountId')), 'itemId': str(data.get('itemId'))}, {
                        '$set': {'Monthly_payment': 0, 'CommtentCount': 0}})


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