import asyncio

from pymongo import MongoClient
from pyppeteer import launch
import redis

r = redis.StrictRedis(host='192.168.1.45', port=6379, db=1, password='admin')
clent = MongoClient('192.168.1.45')
db = clent['pltaobao']
all_goods_detail = db['all_goods_detail']
collection = db['all_tb_anchor_goods_test']


async def dianshangji():
    # 'headless': False如果想要浏览器隐藏更改False为True
    # 127.0.0.1:1080为代理ip和端口，这个根据自己的本地代理进行更改，如果是vps里或者全局模式可以删除掉'--proxy-server=127.0.0.1:1080'
    browser = await launch({'headless': False, 'ignorehttpserrrors': True, 'dumpio': True,
                            'args': ['--no-sandbox'], })

    page = await browser.newPage()

    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36')
    await page.goto("https://m.dianshangji.com/analyst_mtaobaodaydb/analyst.html?itemid={}".format(576956506479))
    await asyncio.sleep(7)
    date_str = await page.Jx('//*[@id="metrictable"]/tbody/tr')
    seller_count = await page.Jx('//*[@id="metrictable"]/tbody/tr/td[3]')
    for index, html_data in enumerate(date_str):
        print((await (await html_data.getProperty('textContent')).jsonValue())[:10], (await (await seller_count[index].getProperty('textContent')).jsonValue()).replace("(", ' ').replace(")", ' ').split(" "))
    await page.close()
    # while 1:
    #     result = r.spop('liveId:ItemId')
    #     if result:
    #         liveId_ItemId = result.decode('utf-8')
    #         liveId = liveId_ItemId.split(':')[0]
    #         ItemId = liveId_ItemId.split(':')[1]
    #         await page.goto("https://m.dianshangji.com/analyst_mtaobaodaydb/analyst.html?itemid={}".format(ItemId))
    #         await asyncio.sleep(7)
    #         date_str = await page.Jx('//*[@id="metrictable"]/tbody/tr')
    #         seller_count = await page.Jx('//*[@id="metrictable"]/tbody/tr/td[3]')
    #         flag = 0
    #         data = all_goods_detail.find_one({'liveId': str(liveId), 'itemId': str(ItemId)})
    #         if data:
    #             for index, html_data in enumerate(date_str):
    #                 time_str = (await (await html_data.getProperty('textContent')).jsonValue())[:10]
    #                 if time_str == data.get('createTime')[:10]:
    #                     flag = 1
    #                     l = (await (await seller_count[index].getProperty('textContent')).jsonValue()).replace("(", ' ').replace(")", ' ').split(" ")
    #
    #                     Monthly_payment = int(l[0])
    #                     try:
    #                         CommtentCount = int(l[1])
    #                     except Exception as e:
    #                         CommtentCount = 0
    #                     res = collection.find_one({'liveId': str(data.get('liveId')), 'itemId': str(data.get('itemId'))})
    #                     if not res:
    #                         res = dict(data)
    #                         res['Monthly_payment'] = Monthly_payment
    #                         res['CommtentCount'] = CommtentCount
    #                         collection.insert_one(res)
    #                     break
    #             if flag == 0:
    #                 res = collection.find_one(
    #                     {'liveId': str(data.get('liveId')), 'itemId': str(data.get('itemId'))})
    #                 if not res:
    #                     res = dict(data)
    #                     res['Monthly_payment'] = 0
    #                     res['CommtentCount'] = 0
    #                     collection.insert_one(res)


if __name__ == '__main__':
    url = 'http://huodong.m.taobao.com/act/talent/live.html?id=95890546-25f5-40c2-aa89-9e9dcea3db7e'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(dianshangji())

