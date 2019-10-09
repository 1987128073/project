import redis
from selenium import webdriver as wb
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import time
from config import environments

ops = Options()
ops.add_experimental_option('excludeSwitches', ['enable-automation'])
ops.add_argument('--proxy-server=http://127.0.0.1:8080')
# ops.add_argument('--headless')

browser = wb.Chrome(executable_path='./WebDriver/chromedriver', chrome_options=ops, )
# browser = wb.Remote(
#             command_executor="http://192.168.1.193:4444/wd/hub",
#             desired_capabilities=DesiredCapabilities.CHROME,
#             options=ops
#         )

def get_live_info(env):
    env_dict = environments.get(env)
    r = redis.StrictRedis().from_url(url=env_dict.get('redis_url'))

    while 1:
        result = r.spop('anchorId:liveId')

        if not result:
            continue

        msg = result.decode('utf-8')

        liveId = msg.split(':')[1]
        base_url = "http://huodong.m.taobao.com/act/talent/live.html?id={}".format(liveId)  # 236139179607
        browser.get(url=base_url)

        try:
            browser.find_element_by_xpath('/html/body/div[3]/div/a').click()
        except:
            pass
        time.sleep(2)
        close_browser(browser)


def close_browser(browser):
    # browser.quit()
    pass


if __name__ == '__main__':
    get_live_info('dev')