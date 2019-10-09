import asyncio

import requests
from logs.wirte_logs import Logger
from config import environments
from pymongo import MongoClient
from pyppeteer import launch
import redis

env_dict = environments.get('pro')
r = redis.StrictRedis().from_url(url=env_dict.get('redis_url'))
clent = MongoClient(env_dict.get('mongodb_host'), port=env_dict.get('mongodb_port'))
db = clent['pltaobao']
goods_detail = db['goods_detail']
collection = db['all_tb_anchor_goods_test']


async def dianshangji():
    # 'headless': False如果想要浏览器隐藏更改False为True
    # 127.0.0.1:1080为代理ip和端口，这个根据自己的本地代理进行更改，如果是vps里或者全局模式可以删除掉'--proxy-server=127.0.0.1:1080'
    browser = await launch({'headless': False, 'ignorehttpserrrors': True, 'dumpio': True,
                            'args': ['--no-sandbox'], })

    page = await browser.newPage()

    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36')
    while 1:
        anchorId_status = r.spop('finish_anchorId:status:uid:anchorName:roomId:is_repetition')
        if anchorId_status:
            anchorName = anchorId_status.decode('utf-8').split(':')[3]
            roomId = anchorId_status.decode('utf-8').split(':')[4]
            status = int(anchorId_status.decode('utf-8').split(':')[1])

            if status != 1:
                continue

            is_repetition = int(anchorId_status.decode('utf-8').split(':')[5])
            if is_repetition:
                Logger('zhuboshuju.log', level='info').logger.info(
                    f'已在爬主播{anchorId_status.decode("utf-8").split(":")[0]}{anchorId_status.decode("utf-8").split(":")[3]}')
                requests.post(url=env_dict.get('callback_url'),
                              data={"uid": anchorId_status.decode('utf-8').split(':')[2], 'anchorState': 2,
                                    'anchorName': anchorName, 'roomId': roomId})
                continue

            anchorId = anchorId_status.decode('utf-8').split(':')[0]
            anchor_goods = goods_detail.find({'anchorId': anchorId})

            for data in anchor_goods:
                ItemId = data.get('itemId')
                await page.goto("https://m.dianshangji.com/analyst_mtaobaodaydb/analyst.html?itemid={}".format(ItemId))
                await asyncio.sleep(8)
                date_str = await page.Jx('//*[@id="metrictable"]/tbody/tr')
                seller_count = await page.Jx('//*[@id="metrictable"]/tbody/tr/td[3]')
                flag = 0
                for index, html_data in enumerate(date_str):
                    time_str = (await (await html_data.getProperty('textContent')).jsonValue())[:10]
                    if time_str == data.get('createTime')[:10]:
                        flag = 1
                        l = (await (await seller_count[index].getProperty('textContent')).jsonValue()).replace("(", ' ').replace(")", ' ').split(" ")

                        Monthly_payment = int(l[0])
                        # 如果异常，则无CommtentCount数据，默认为0
                        try:
                            CommtentCount = int(l[1])
                        except Exception as e:
                            CommtentCount = 0

                        res = collection.find_one(
                            {'liveId': str(data.get('liveId')), 'itemId': str(data.get('itemId'))})
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
            if anchor_goods:
                r.sadd('anchorId:status', f'{anchorId}:{1}')
                collection.update({"anchorId": str(anchorId)}, {'$set': {"is_dispose": 3}})
                requests.post(url=env_dict.get('callback_url'),
                              data={"uid": anchorId_status.decode('utf-8').split(':')[2], 'anchorState': 2,
                                    'anchorName': anchorName, 'roomId': roomId})
            else:
                r.sadd('anchorId:status', f'{anchorId}:{0}')


if __name__ == '__main__':
    url = 'http://huodong.m.taobao.com/act/talent/live.html?id=95890546-25f5-40c2-aa89-9e9dcea3db7e'
    asyncio.get_event_loop().run_until_complete(dianshangji())
