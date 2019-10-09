import datetime
import time
import redis
import requests
from pymongo import MongoClient
from selenium import webdriver as wb
from config import environments
from wirte_logs import Logger


class DianShangJi(object):
    '''
    爬取zhiboshuju.com网站的主播7天带货数据
    '''
    def __init__(self, env):
        self.clent = MongoClient('192.168.1.45')
        self.db = self.clent['pltaobao']
        self.goods_detail = self.db['goods_detail']
        self.all_goods_detail = self.db['all_goods_detail']
        self.collection = self.db['all_tb_anchor_goods_test']
        self.r = redis.StrictRedis().from_url(url=environments.get(env).get('redis_url'))
        self.browser = wb.Edge()
        self.base_url = 'https://m.dianshangji.com/analyst_mtaobaodaydb/analyst.html?itemid={}#itemid={}'

    def get_sellCount(self):
        '''
        定时更新全部主播带货数据
        :return:
        '''
        while 1:
            liveId_ItemId = self.r.spop('liveId:ItemId')
            if liveId_ItemId:
                liveId = liveId_ItemId.decode('utf-8').split(':')[0]
                ItemId = liveId_ItemId.decode('utf-8').split(':')[1]

                # if not self.check_task(anchorId_ItemId.decode('utf-8')):
                #     continue

                self.browser.get(self.base_url.format(ItemId, ItemId))
                time.sleep(8)
                html_data = self.browser.find_elements_by_xpath('//table[@id="metrictable"]/tbody/tr')
                flag = 0
                data = self.all_goods_detail.find_one({'liveId': str(liveId), 'itemId': str(ItemId)})
                if data:
                    for a in html_data:
                        if a.text[:10] == data.get('createTime')[:10]:
                            flag = 1
                            l = a.text.split(' ')
                            Monthly_payment = int(l[2].split('\n')[0])
                            try:
                                CommtentCount = int(l[2].split('\n')[-2].replace('(', '').replace(')', ''))
                            except Exception as e:
                                # Logger('./logs/DianShangJi.log', level='error').logger.info(
                                #     f'CommtentCount_Exception:{e}')
                                CommtentCount = 0
                            res = self.collection.find_one({'liveId': str(data.get('liveId')), 'itemId': str(data.get('itemId'))})
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

    def get_anchor_data(self, anchorId):
        res = self.goods_detail.find({'anchorId': anchorId})
        anchor_goods = []
        for data in res:
            anchor_goods.append(data)
        return anchor_goods

    def get_sellCount2(self):
        while 1:
            anchorId_status = self.r.spop('finish_anchorId:status:uid')
            if anchorId_status:
                status = int(anchorId_status.decode('utf-8').split(':')[1])
                if status != 1:
                    continue

                anchorId = anchorId_status.decode('utf-8').split(':')[0]
                anchor_goods = self.get_anchor_data(anchorId)
                for data in anchor_goods:
                    ItemId = data.get('itemId')
                    self.browser.get(self.base_url.format(ItemId, ItemId))
                    time.sleep(8)
                    html_data = self.browser.find_elements_by_xpath('//table[@id="metrictable"]/tbody/tr')
                    flag = 0
                    for a in html_data:
                        if a.text[:10] == data.get('createTime')[:10]:
                            flag = 1
                            l = a.text.split(' ')
                            Monthly_payment = int(l[2].split('\n')[0])
                            try:
                                CommtentCount = int(l[2].split('\n')[-2].replace('(', '').replace(')', ''))
                            except:
                                break
                            res = self.collection.find_one({'liveId': str(data.get('liveId')), 'itemId': str(data.get('itemId'))})
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
                    self.send_sign(anchorId_status.decode('utf-8').split(':')[2], 2)
                else:
                    self.r.sadd('anchorId:status', f'{anchorId}:{0}')

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

    def send_sign(self, uid, num):
        requests.post(url='http://test.pl298.com:8007/analysis/updateUser', data={"uid": uid, 'anchorState': num})
        pass


if __name__ == '__main__':
    dsj = DianShangJi(env='dev')
    dsj.run()