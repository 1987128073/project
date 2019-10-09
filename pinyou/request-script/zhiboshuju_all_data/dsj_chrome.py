import time
from selenium import webdriver as wb
from pymongo import MongoClient
import redis
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


r = redis.StrictRedis(host='192.168.1.45', port=6379, db=1, password='admin')
clent = MongoClient('192.168.1.45')
db = clent['pltaobao']
all_goods_detail = db['all_goods_detail']
collection = db['all_tb_anchor_goods_test']
browser = wb.Remote(
            command_executor="http://192.168.1.63:30004/wd/hub",
            desired_capabilities=DesiredCapabilities.CHROME
        )
url = 'https://m.dianshangji.com/analyst_mtaobaodaydb/analyst.html?itemid={}'


def dianshangji():

    while 1:
        result = r.spop('liveId:ItemId')
        if result:
            liveId_ItemId = result.decode('utf-8')
            liveId = liveId_ItemId.split(':')[0]
            ItemId = liveId_ItemId.split(':')[1]
            print(f'正在爬：{liveId}:{ItemId}')
            try:
                browser.get(url=url.format(ItemId))
                time.sleep(6)
                date_str = browser.find_elements_by_xpath('//*[@id="metrictable"]/tbody/tr')
                seller_count = browser.find_elements_by_xpath('//*[@id="metrictable"]/tbody/tr/td[3]')
                flag = 0
                data = all_goods_detail.find_one({'liveId': str(liveId), 'itemId': str(ItemId)})
                if data:
                    for index, html_data in enumerate(date_str):

                        if html_data.text[:10] == data.get('createTime')[:10]:
                            flag = 1
                            l = seller_count[index].text.replace("(", ' ').replace("\n", '').replace(")", ' ').split(" ")

                            Monthly_payment = int(l[0])
                            try:
                                CommtentCount = int(l[1])
                            except Exception as e:
                                CommtentCount = 0

                            print(Monthly_payment, CommtentCount)
                            res = collection.find_one({'liveId': str(data.get('liveId')), 'itemId': str(data.get('itemId'))})
                            if not res:
                                res = dict(data)
                                res['Monthly_payment'] = Monthly_payment
                                res['CommtentCount'] = CommtentCount
                                collection.insert_one(res)
                            break
                    if flag == 0:
                        res = collection.find_one(
                            {'liveId': str(data.get('liveId')), 'itemId': str(data.get('itemId'))})
                        if not res:
                            res = dict(data)
                            res['Monthly_payment'] = 0
                            res['CommtentCount'] = 0
                            collection.insert_one(res)
            except:
                r.sadd('liveId:ItemId', liveId_ItemId)
                continue


if __name__ == '__main__':
    dianshangji()

