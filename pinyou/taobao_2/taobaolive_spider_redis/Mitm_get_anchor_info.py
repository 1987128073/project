import time
import redis
from selenium import webdriver as wb
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from config import environments
from utils.sign import send_sign

ops = Options()
ops.add_experimental_option('excludeSwitches', ['enable-automation'])
ops.add_argument('--proxy-server=http://127.0.0.1:8080')
# ops.add_argument('--allow-running-insecure-content')  # 设置proxy时添加的额外参数，允许不安全的证书
# ops.add_argument('--ignore-certificate-errors')  # 设置proxy时添加的额外参数，允许不安全的证书
# ops.add_argument('--headless')

browser = wb.Chrome(executable_path='./WebDriver/chromedriver', chrome_options=ops, )
# browser = wb.Remote(
#             command_executor="http://127.0.0.1:4444/wd/hub",
#             desired_capabilities=DesiredCapabilities.CHROME,
#             options=ops
#         )


def get_anchor_info(env):
    env_dict = environments.get(env)
    r = redis.StrictRedis().from_url(url=env_dict.get('redis_url'))
    while 1:
        result = r.spop('anchorId:anchorName:uid:roomId:env')

        if not result:
            continue

        msg = result.decode('utf-8')

        anchorId = msg.split(':')[0]
        uid = msg.split(':')[2]
        anchorName = msg.split(':')[1]
        roomId = msg.split(':')[3]
        env = msg.split(':')[-1]
        base_url = 'https://market.m.taobao.com/apps/abs/9/41/index?accountId={}'.format(anchorId)  # https://market.m.taobao.com/apps/abs/9/41/index?accountId=159539916
        browser.get(url=base_url)
        time.sleep(0.5)
        # 查询主播可能无数据
        try:
            fans_count = browser.find_element_by_xpath('//*[@id="abs-block"]/div/div[3]/div/div[3]/div/span[1]/text()')
        except:
            fans_count = 'NaN'
            close_browser(browser)

        if fans_count != 'NaN':
            send_sign(uid, env, anchorName, roomId, num=1)
        else:
            send_sign(uid, env, anchorName, roomId, num=3)
            continue

        try:
            target = browser.find_element_by_xpath('//*[@id="abs-block"]/div/div[14]')
            browser.execute_script("arguments[0].scrollIntoView();", target)
        except:
            close_browser(browser)
            continue

        time.sleep(0.5)
        close_browser(browser)


def close_browser(browser):
    # browser.quit()
    pass


if __name__ == '__main__':
    get_anchor_info('dev')