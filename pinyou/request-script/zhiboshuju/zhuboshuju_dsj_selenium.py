import datetime
import time
import redis
import requests
from pymongo import MongoClient
from selenium import webdriver as wb
from config import environments
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class DianShangJi(object):

    def __init__(self, env):
        self.env_dict = environments.get(env)
        self.callback_url = self.env_dict.get('callback_url')
        self.clent = MongoClient(self.env_dict.get('mongodb_host'), port=self.env_dict.get('mongodb_port'))
        self.db = self.clent['pltaobao']
        self.goods_detail = self.db['goods_detail']
        self.all_goods_detail = self.db['all_goods_detail']
        self.collection = self.db['all_tb_anchor_goods_test']
        self.r = redis.StrictRedis().from_url(url=self.env_dict.get('redis_url'))
        # self.browser = wb.Chrome()
        self.browser = wb.Remote(
            command_executor="http://127.0.0.1:4444/wd/hub",
            desired_capabilities=DesiredCapabilities.CHROME
        )
        self.base_url = 'https://m.dianshangji.com/analyst_mtaobaodaydb/analyst.html?itemid={}'

    def get_anchor_data(self, anchorId):
        res = self.goods_detail.find({'anchorId': anchorId})
        anchor_goods = []
        for data in res:
            anchor_goods.append(data)
        return anchor_goods

    def test(self):

        self.browser.get(self.base_url.format('590755610830'))
        time.sleep(6)
        date_str = self.browser.find_elements_by_xpath('//*[@id="metrictable"]/tbody/tr')
        seller_count = self.browser.find_elements_by_xpath('//*[@id="metrictable"]/tbody/tr/td[3]')
        for index, html_data in enumerate(date_str):
                print(html_data.text[:10], seller_count[index].text.replace("(", ' ').replace("\n", '').replace(")", ' ').split(" "))
        self.browser.close()

    def get_sellCount2(self):

        while 1:
            anchorId_status = self.r.spop('finish_anchorId:status:uid:anchorName:roomId:is_repetition')
            if anchorId_status:
                self.anchorName = anchorId_status.decode('utf-8').split(':')[3]
                self.roomId = anchorId_status.decode('utf-8').split(':')[4]
                status = int(anchorId_status.decode('utf-8').split(':')[1])
                is_repetition = int(anchorId_status.decode('utf-8').split(':')[5])

                if status != 1:
                    continue

                if is_repetition:
                    self.send_sign(anchorId_status.decode('utf-8').split(':')[2], 2)
                    continue

                anchorId = anchorId_status.decode('utf-8').split(':')[0]
                anchor_goods = self.get_anchor_data(anchorId)
                for data in anchor_goods:
                    ItemId = data.get('itemId')
                    self.browser.get(self.base_url.format(ItemId))
                    time.sleep(6)
                    date_str = self.browser.find_elements_by_xpath('//*[@id="metrictable"]/tbody/tr')
                    seller_count = self.browser.find_elements_by_xpath('//*[@id="metrictable"]/tbody/tr/td[3]')
                    flag = 0
                    for index, html_data in enumerate(date_str):
                        if html_data.text[:10] == data.get('createTime')[:10]:
                            flag = 1
                            l = seller_count[index].text.replace("(", ' ').replace("\n", '').replace(")", ' ').split(" ")

                            Monthly_payment = int(l[0])
                            try:
                                CommtentCount = int(l[1])
                            except Exception as e:
                                CommtentCount = 0

                            res = self.collection.find_one(
                                {'liveId': str(data.get('liveId')), 'itemId': str(data.get('itemId'))})
                            if not res:
                                res = dict(data)
                                res['Monthly_payment'] = Monthly_payment
                                res['CommtentCount'] = CommtentCount

                                self.collection.insert_one(res)
                            break
                    if flag == 0:
                        res = self.collection.find_one(
                            {'liveId': str(data.get('liveId')), 'itemId': str(data.get('itemId'))})
                        if not res:
                            res = dict(data)
                            res['Monthly_payment'] = 0
                            res['CommtentCount'] = 0

                            self.collection.insert_one(res)

                if anchor_goods:
                    self.r.sadd('anchorId:status', f'{anchorId}:{1}')
                    self.update_is_dispose(anchorId)
                    self.send_sign(anchorId_status.decode('utf-8').split(':')[2], 2)
                else:
                    self.r.sadd('anchorId:status', f'{anchorId}:{0}')
                    pass

    def update_is_dispose(self, anchorId):
        self.collection.update_many({"anchorId": str(anchorId)}, {'$set': {"is_dispose": 3}})
        pass

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
        self.get_sellCount2()
        self.__close()

    def send_sign(self, uid, num):
        requests.post(url=self.callback_url,
                      data={"uid": int(uid), 'anchorState': num, 'anchorName': self.anchorName, 'roomId': self.roomId})
        pass


if __name__ == '__main__':
    dsj = DianShangJi(env='pro')
    dsj.run()
