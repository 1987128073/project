import time

from selenium import webdriver as wb
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

ops = Options()
ops.add_experimental_option('excludeSwitches', ['enable-automation'])
ops.add_argument('--proxy-server=http://192.168.1.121:8080')
browser = wb.Chrome(chrome_options=ops, )
# browser = wb.Remote(
#             command_executor="http://192.168.1.63:32100/wd/hub",
#             desired_capabilities=DesiredCapabilities.CHROME,
#             options=ops
#         )
browser.get(url='http://mitm.it')
time.sleep(30)
browser.close()