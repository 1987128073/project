import csv
import time

import requests
import xlutils
import xlwt
from pymongo import MongoClient
from requests.auth import HTTPProxyAuth
import xlrd

class Brand_spider(object):

    def __init__(self):
        self.url = 'https://acs.m.taobao.com/gw/mtop.taobao.detail.getdetail/6.0/?data=%7B"itemNumId"%3A"{}"%7D'
        self.headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
        }
        self.proxies = {
            'http': 'http://http-proxy-t1.dobel.cn:9180'
        }
        self.auth = HTTPProxyAuth('ATLANDG4EGPK5S0', 'LKHN5uFx')
        self.db = MongoClient('192.168.1.45')['pltaobao']
        self.collection = self.db['BrandInfo']
        self.list = []

    def get_data(self):
        for id in self.list:
            response = requests.get(url=self.url.format(id),
                                    headers=self.headers, proxies=self.proxies, auth=self.auth,).json()
            if response.get('data').get('item'):
                itemId = response.get('data').get('item').get('itemId')
                print(itemId)
                brandId = response.get('data').get('params').get('trackParams').get('brandId')

                try:
                    brand = response.get('data').get('props').get('groupProps')[0].get('基本信息')
                except:
                    try:
                        brand = response.get('data').get('props').get('propsList')[0].get('baseProps')
                    except:
                        brand = None
                if brand:
                    for a in brand:
                        for k, v in a.items():
                            if k=='品牌':
                                brandname = v
                                self.save(brandId, brandname, itemId)
                time.sleep(3)

    def save(self, brandId, brandname, itemId):
        res = self.collection.find_one({'itemId': str(itemId)})
        if not res:
            data = {

                'brandId': str(brandId),
                'brandname': brandname,
                'itemId': str(itemId),
            }
            self.collection.insert_one(data)

    def get_xlsx_data(self):
        x1 = xlrd.open_workbook("goods.xlsx")
        sheet1 = x1.sheet_by_name("Sheet1")
        for i in range(1, sheet1.nrows):

            self.list.append(sheet1.row_values(i)[12].split('=')[1])


    def run(self):

        self.get_xlsx_data()
        self.get_data()

if __name__ == '__main__':
    brandspider = Brand_spider()
    brandspider.run()

