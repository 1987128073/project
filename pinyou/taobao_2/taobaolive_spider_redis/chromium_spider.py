import asyncio

import redis
from pyppeteer import launch

from config import environments


async def get_anchor_info(env):
    env_dict = environments.get(env)
    r = redis.StrictRedis().from_url(url=env_dict.get('redis_url'))

    browser = await launch({'headless': True, 'ignorehttpserrrors': True, 'dumpio': True,
                            'args': ['--no-sandbox', '--proxy-server=127.0.0.1:8080']})

    page = await browser.newPage()
    while 1:
        result = r.spop('anchorId:anchorName:uid:roomId')

        if not result:
            continue

        msg = result.decode('utf-8')
        anchorId = msg.split(':')[0]
        # 'headless': False如果想要浏览器隐藏更改False为True
        # 127.0.0.1:1080为代理ip和端口，这个根据自己的本地代理进行更改，如果是vps里或者全局模式可以删除掉'--proxy-server=127.0.0.1:1080'


        await page.setUserAgent(
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36')

        await page.goto('https://market.m.taobao.com/apps/abs/9/41/index?accountId={}'.format(anchorId))  # 159539916
        try:
            await page.click('body > div.J_MIDDLEWARE_FRAME_WIDGET > div > a')
        except:
            pass
        await page.waitFor(3000)


async def get_live_info(env):
    env_dict = environments.get(env)
    r = redis.StrictRedis().from_url(url=env_dict.get('redis_url'))

    browser = await launch({'headless': True, 'ignorehttpserrrors': True, 'dumpio': True,
                            'args': ['--no-sandbox', '--proxy-server=127.0.0.1:8080']})

    page = await browser.newPage()
    while 1:
        result = r.spop('anchorId:liveId')

        if not result:
            continue

        msg = result.decode('utf-8')
        liveId = msg.split(':')[1]
        # 'headless': False如果想要浏览器隐藏更改False为True
        # 127.0.0.1:1080为代理ip和端口，这个根据自己的本地代理进行更改，如果是vps里或者全局模式可以删除掉'--proxy-server=127.0.0.1:1080'

        await page.setUserAgent(
            'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36')

        await page.goto("http://huodong.m.taobao.com/act/talent/live.html?id={}".format(liveId))  # 236139179607
        try:
            await page.click('body > div.J_MIDDLEWARE_FRAME_WIDGET > div > a')
        except:
            pass
        await page.waitFor(3000)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(get_anchor_info('dev'))