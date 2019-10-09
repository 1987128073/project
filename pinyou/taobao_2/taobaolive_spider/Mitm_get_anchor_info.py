import time

from selenium import webdriver as wb
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from receive_msg import ConsumingMsg
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


def get_anchor_info(msg):
    anchorId = msg.split(':')[0]
    uid = msg.split(':')[2]
    anchorName = msg.split(':')[1]
    roomId = msg.split(':')[3]
    env = msg.split(':')[-1]
    base_url = 'https://market.m.taobao.com/apps/abs/9/41/index?accountId={}'.format(anchorId)  # 159539916
    browser.get(url=base_url)
    time.sleep(0.5)
    # 查询主播可能无数据
    try:
        anchor_name = browser.find_element_by_xpath('//*[@id="abs-block"]/div/div[3]/div/div[2]/div[1]/span/text()')
    except:
        anchor_name = None
        close_browser(browser)

    if anchor_name is None:
        send_sign(uid, env, anchorName, roomId, num=3)
        close_browser(browser)
        return

    send_sign(uid, env, anchorName, roomId, num=1)

    try:
        target = browser.find_element_by_xpath('//*[@id="abs-block"]/div/div[14]')
        browser.execute_script("arguments[0].scrollIntoView();", target)
    except:
        close_browser(browser)
        return
    time.sleep(0.5)
    close_browser(browser)
    return


def close_browser(browser):
    # browser.quit()
    pass


if __name__ == '__main__':
    cm = ConsumingMsg(queue_name='anchorId:anchorName:uid:roomId', env='dev', func=get_anchor_info)
    cm.consuming_task()