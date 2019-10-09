import re

import requests
from requests.adapters import HTTPAdapter

class TmallSpider(object):

    def __init__(self):
        self.url = 'https://detail.tmall.com/item.htm?id={}'
        self.taobao_goods_url = 'https://item.taobao.com/item.htm?ft=t&id={}'
        auth = {}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
        }

    def getid(self, itemid):
        # print(itemid)

        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))
        try:
            response = s.get(url=self.taobao_goods_url.format(itemid), headers=self.headers, timeout=5)
        except requests.exceptions.RequestException as e:
            categoryId = None
            rootCatId = None
            shopId = None
            shop_name = None
            buy_enable = False
            flag = 0
            return categoryId, rootCatId, shopId, shop_name, buy_enable, flag

        if response.status_code in [404, 403]:
            categoryId = None
            rootCatId = None
            shopId = None
            shop_name = None
            buy_enable = False
            flag = 1
            return categoryId, rootCatId, shopId, shop_name, buy_enable, flag

        # response = requests.get(url=self.taobao_goods_url.format(itemid))
        if '很抱歉，您查看的宝贝不存在' in response.text:
            categoryId = None
            rootCatId = None
            shopId = None
            shop_name = None
            buy_enable = False
            flag = 0
            return categoryId, rootCatId, shopId, shop_name, buy_enable, flag

        # categoryId_pattern = re.compile(r',categoryId:(\d*?),', re.S)
        # rootCatId_pattern = re.compile(r'name="rootCatId" value="(\d*?)"', re.S)

        cid_pattern = re.compile(r" cid\s*: '(\d*?)'", re.S)
        rcid_pattern = re.compile(r"rcid\s*: '(\d*?)'", re.S)
        shopId_pattern = re.compile(r" shopId\s*: '(\d*?)'", re.S)
        shop_name_pattern = re.compile(r" shopName\s*: '(.*?)'", re.S)
        status_pattern = re.compile(r" status\s*: (.*?),", re.S)
        try:
            categoryId = int(re.search(cid_pattern, response.text).group(1))
        except:
            categoryId = None

        try:
            rootCatId = int(re.search(rcid_pattern, response.text).group(1))
        except:
            rootCatId = None

        try:
            shopId = int(re.search(shopId_pattern, response.text).group(1))
        except:
            shopId = None

        try:
            shop_name = re.search(shop_name_pattern, response.text).group(1)
        except:
            shop_name = None
        try:
            status = int(re.search(status_pattern, response.text).group(1))
        except:
            status = -2

        if status == 0:
            buy_enable = True
        else:
            buy_enable = False
        flag = 0
        print(categoryId, rootCatId, shopId, shop_name, buy_enable)
        return categoryId, rootCatId, shopId, shop_name, buy_enable, flag


if __name__ == '__main__':
    TM = TmallSpider()
    itemid = 600024278481
    TM.getid(itemid)