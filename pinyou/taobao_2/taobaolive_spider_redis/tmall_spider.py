import re
import time
from urllib import parse
import requests
from requests.adapters import HTTPAdapter
from requests.auth import HTTPProxyAuth


class TmallSpider(object):

    def __init__(self):
        self.tmall_url = 'https://detail.tmall.com/item.htm?id={}'
        self.taobao_goods_url = 'https://item.taobao.com/item.htm?ft=t&id={}'
        self.proxy = {'http': 'http-dyn.abuyun.com:9020'}
        self.auth = HTTPProxyAuth('HG3T29V0U33H432D', 'CF9328D54686ED24')
        self.headers = {
            # 'accept-encoding': 'gzip, deflate, br',
            # 'accept-language': 'zh-CN,zh;q=0.9',
            # 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            # 'Cookie': 'enc=VfS9pXV44E9bUOwMfVUhsI2f5KZoEWQRTTlmnAHeMuXbeGacMJCCOJLBAJ3Yg9wnm1mkcs7CYgKbLwwkj7b6zw%3D%3D;'
        }

    def getid(self, itemid):
        # print(itemid)

        response = requests.get(url=self.tmall_url.format(itemid), headers=self.headers, allow_redirects=False)
        print(response.status_code, )
        try:
            response = requests.get(url=self.tmall_url.format(itemid), headers=self.headers, timeout=3, allow_redirects=False)
        except requests.exceptions.RequestException as e:
            categoryId = None
            rootCatId = None
            shopId = None
            shop_name = None
            buy_enable = False
            flag = 1
            return categoryId, rootCatId, shopId, shop_name, buy_enable, flag

        if response.status_code in [404, 403]:
            time.sleep(1.8)
            response = requests.get(url=self.taobao_goods_url.format(itemid), headers=self.headers, timeout=3,)
            print(response.status_code)
            try:
                response = requests.get(url=self.taobao_goods_url.format(itemid), headers=self.headers, timeout=3)
            except requests.exceptions.RequestException as e:
                categoryId = None
                rootCatId = None
                shopId = None
                shop_name = None
                buy_enable = False
                flag = 1
                return categoryId, rootCatId, shopId, shop_name, buy_enable, flag

        if 'deny cc' in response.text:
            categoryId = None
            rootCatId = None
            shopId = None
            shop_name = None
            buy_enable = False
            flag = 1
            return categoryId, rootCatId, shopId, shop_name, buy_enable, flag

        if '很抱歉，您查看的宝贝不存在' in response.text:
            categoryId = None
            rootCatId = None
            shopId = None
            shop_name = None
            buy_enable = False
            flag = 0
            return categoryId, rootCatId, shopId, shop_name, buy_enable, flag

        if 'tmall.com' in response.url:
            cid_pattern = re.compile(r',categoryId:(\d*?),', re.S)
            rcid_pattern = re.compile(r'name="rootCatId" value="(\d*?)"', re.S)
            shopId_pattern = re.compile(r"; shopId=(\d*?);", re.S)
            shop_name_pattern = re.compile(r'sellerNickName:"(.*?)",', re.S)
            brand_name = re.compile(r'"brand":"(.*?)",', re.S)
            brand_id = re.compile(r',"brandId":"(.*?)",', re.S)
            status_pattern = re.compile(r'"auctionStatus":"(.*?)",', re.S)
        else:
            cid_pattern = re.compile(r" cid\s*: '(\d*?)'", re.S)
            rcid_pattern = re.compile(r"rcid\s*: '(\d*?)'", re.S)
            shopId_pattern = re.compile(r" shopId\s*: '(\d*?)'", re.S)
            shop_name_pattern = re.compile(r" shopName\s*: '(.*?)'", re.S)
            status_pattern = re.compile(r" status\s*: (.*?),", re.S)
            brand_name = re.compile(r'"brand":"(.*?)",', re.S)
            brand_id = re.compile(r',"brandId":"(.*?)",', re.S)

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
            shop_name = parse.unquote(shop_name)
            print(shop_name)
        except:
            shop_name = None

        try:
            brand_name = re.search(brand_name, response.text).group(1)
            print(type(brand_name))
            brand_name = parse.unquote(brand_name)
            print(brand_name)
        except:
            brand_name = None

        try:
            brand_id = int(re.search(brand_id, response.text).group(1))
        except:
            brand_id = None

        try:
            status = int(re.search(status_pattern, response.text).group(1))
        except:
            status = -2

        if status == 0:
            buy_enable = True
        else:
            buy_enable = False
        flag = 0
        print('categoryId:{}, rootCatId:{}, shopId:{}, shop_name:{}, buy_enable:{},brand_id:{}, brand_name:{}'.format(categoryId, rootCatId, shopId, shop_name, buy_enable, brand_id, brand_name))
        return categoryId, rootCatId, shopId, shop_name, buy_enable, flag


if __name__ == '__main__':
    TM = TmallSpider()
    itemid = 600024278481
    TM.getid(itemid)