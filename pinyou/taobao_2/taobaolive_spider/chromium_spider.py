import asyncio
from pyppeteer import launch

from receive_msg import ConsumingMsg


async def main1(msg):
    liveId = msg.split(':')[1]
    # 'headless': False如果想要浏览器隐藏更改False为True
    # 127.0.0.1:1080为代理ip和端口，这个根据自己的本地代理进行更改，如果是vps里或者全局模式可以删除掉'--proxy-server=127.0.0.1:1080'
    browser = await launch({'headless': True, 'ignorehttpserrrors': True, 'dumpio': True,
                            'args': ['--no-sandbox', '--proxy-server=127.0.0.1:8080']})

    page = await browser.newPage()

    await page.setUserAgent(
        'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36')

    await page.goto("http://huodong.m.taobao.com/act/talent/live.html?id={}".format(liveId))
    try:
        await page.click('body > div.J_MIDDLEWARE_FRAME_WIDGET > div > a')
    except:
        pass
    await page.waitFor(3000)


if __name__ == '__main__':
    cm = ConsumingMsg(queue_name='anchorId:liveId', env='dev', func=main1)
    cm.consuming_task()
    asyncio.get_event_loop().run_until_complete(main1(msg))