# -*- coding: utf-8 -*-
import base64

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent


class GetData(object):

    def __init__(self):
        self.ua = UserAgent()
        self.browser = webdriver.Chrome()
        self.ops = Options()
        self.ops.add_argument('--headless')
        self.ops.add_extension("proxy.zip")
        self.proxy = 'http-proxy-t1.dobel.cn:9180'
        self.ops.add_argument(f'--proxy-server=http://{self.proxy}')

    def selenium_open_url(self):
        self.browser.get("http://www.baidu.com")
        # self.browser.get("http://huodong.m.taobao.com/act/talent/live.html?userId=724930645")
        self.browser.delete_all_cookies()

    def save_data(self):
        pass

    def __close(self):
        self.browser.quit()

    def run(self):
        self.selenium_open_url()
        self.__close()


if __name__ == '__main__':
    getdata = GetData()
    getdata.run()