import redis
from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep


class taobao_infos:

    WIDTH = 320
    HEIGHT = 640
    PIXEL_RATIO = 3.0
    UA = 'Mozilla/5.0 (Linux; Android 4.1.1; GT-N7100 Build/JRO03C) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/35.0.1916.138 Mobile Safari/537.36 T7/6.3'

    mobileEmulation = {"deviceMetrics": {"width": WIDTH, "height": HEIGHT, "pixelRatio": PIXEL_RATIO}, "userAgent": UA}

    def __init__(self, url):
        self.url = 'https://login.m.taobao.com/login.htm?spm=0.0.0.0&nv=true&redirectURL=https%3A%2F%2Ftaobaolive.taobao.com%2Froom%2Findex.htm%3Fspm%3Da21tn.8216370.2278281.2.4bee5722jVAZZN%26feedId%3D232243582857&loginFrom=wap_tbTop'

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option('mobileEmulation', self.mobileEmulation)
        options.add_argument("--proxy-server=http://192.168.1.63:30800")
        self.browser = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.browser, 10)
        self.db = MongoClient('192.168.1.180', port=32766)['pltaobao']
        self.collection = self.db['CommoditySalesInfo']
        self.r = redis.StrictRedis(host='192.168.1.45',password='admin')

    # 处理登陆信息
    def login(self):
        self.browser.get(self.url)
        sleep(3)
        self.browser.find_element_by_class_name('ft-left').click()
        sleep(8)
        self.browser.find_element_by_name('TPL_username').send_keys('13167617973')
        sleep(3)
        self.browser.find_element_by_id('getCheckcode').click()
        sleep(3)
        self.browser.find_element_by_link_text('账户密码登录').click()
        sleep(3)
        self.browser.find_element_by_name('TPL_username').send_keys('13167617973')
        self.browser.find_element_by_name('TPL_password').send_keys('zc123456789')
        self.browser.find_element_by_link_text('登录').click()
        sleep(10)

        # while 1:
        #     liveid = self.r.spop('liveid')
        #     if not liveid:
        #         sleep(5)
        #     else:
        #         self.browser.get('https://taobaolive.taobao.com/room/index.htm?feedId={}'.format(liveid.decode('utf-8')))
        #         sleep(10)
        #         live_goods_title = self.browser.find_elements_by_xpath('//*[@id="J_item_wrapper"]/ul/li/div/a/div[2]/div[1]')
        #         live_goods_sales = self.browser.find_elements_by_xpath('//*[@id="J_item_wrapper"]/ul/li/div/a/div[2]/div[3]')
        #         live_goods_price = self.browser.find_elements_by_xpath('//*[@id="J_item_wrapper"]/ul/li/div/a/div[2]/div[2]/b')
        #         try:
        #             itemid = self.browser.find_elements_by_xpath('//*[@id="J_item_wrapper"]/ul/li/div/a/@href')
        #         except:
        #             itemid = None
        #         l = []
        #         if not itemid:
        #             for a, b, c in zip(live_goods_title, live_goods_sales, live_goods_price):
        #                 item = {}
        #                 item['live_goods_title'] = a.text
        #                 item['live_goods_sales'] = int(b.text.split('人')[0])
        #                 item['live_goods_price'] = int(c.text)
        #                 item['itemurl'] = None
        #                 l.append(item)
        #                 print(liveid.decode('utf-8'), l)
        #
        #                 self.save_data1(liveid.decode('utf-8'), l)
        #         else:
        #             for a,b,c,d in zip(live_goods_title, live_goods_sales, live_goods_price, itemid):
        #                 item = {}
        #                 item['live_goods_title'] = a.text
        #                 item['live_goods_sales'] = int(b.text.split('人')[0])
        #                 item['live_goods_price'] = int(c.text)
        #                 item['itemurl'] = str(d.text)
        #                 l.append(item)
        #                 print(liveid.decode('utf-8'), l)
        #                 self.save_data(liveid.decode('utf-8'),l)
        #         sleep(20)

    def save_data(self, liveId, l):
        res = self.collection.find({'liveId': liveId})
        if not res:
            data = {
                'liveId': liveId,
                 'live_goods_title': l,
            }
            self.collection.insert_one(data)

    def save_data1(self, liveId, l):
        res = self.collection.find({'liveId': liveId})
        if not res:
            data = {
                'liveId': liveId,
                'live_goods_title': l,
            }
            self.collection.insert_one(data)

url = 'https://login.taobao.com/member/login.jhtml'
a = taobao_infos(url)
a.login()