import asyncio
import time

from pyppeteer import launch
import redis

from logs.wirte_logs import Logger

r = redis.StrictRedis(host='192.168.1.180', port=30378, db=0)


async def taobaolive():
    # 'headless': False如果想要浏览器隐藏更改False为True
    # 127.0.0.1:1080为代理ip和端口，这个根据自己的本地代理进行更改，如果是vps里或者全局模式可以删除掉'--proxy-server=127.0.0.1:1080'
    browser = await launch({'headless': True, 'ignorehttpserrrors': True, 'dumpio': True,
                            'args': ['--no-sandbox', '--proxy-server=127.0.0.1:8080']})

    page = await browser.newPage()

    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36')


    await page.goto("http://huodong.m.taobao.com/act/talent/live.html?id={}".format(234916199277))
    await page.click('body > div.J_MIDDLEWARE_FRAME_WIDGET > div > a')
    await page.waitFor(2000)

if __name__ == '__main__':
    url = 'http://huodong.m.taobao.com/act/talent/live.html?id=95890546-25f5-40c2-aa89-9e9dcea3db7e'
    loop = asyncio.get_event_loop()
    loop.run_until_complete(taobaolive())
