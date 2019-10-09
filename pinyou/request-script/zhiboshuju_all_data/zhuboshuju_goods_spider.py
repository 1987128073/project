import time

import pymysql
import redis
import requests
from pymongo import MongoClient
from config import environments


class GoodsSpider(object):
    '''
    抓取zhiboshuju.com网站的主播7天带货数据
    '''

    def __init__(self, env):

        self.r = redis.StrictRedis().from_url(url=environments.get(env).get('redis_url'))
        # self.r = redis.StrictRedis().from_url(url='redis://:admin@192.168.1.45:6379/1')
        self.client = MongoClient('192.168.1.45')
        self.db = self.client['pltaobao']
        self.collection = self.db['all_goods_detail']
        self.mysqldb = pymysql.connect(host='212.64.84.172',  # 数据库服务器IP
                             port=3306,
                             user='plceshi',
                             passwd='Plceshi2018',
                             db='pinliang_test')  # 数据库名称
        self.cur = self.mysqldb.cursor()  # 游标

    def _close_mysql_conn(self):

        self.mysqldb.close()

    def select_goods_categoryId(self, catId):
        self.mysqldb.ping(reconnect=True)

        # 使用execute()执行SQL语句
        self.cur.execute("select category from pl_taobao_category where tao_leaf_category_id={}".format(catId))

        # 使用 fetchone() 方法获取一条数据
        data = self.cur.fetchone()

        if not data:
            catId = 2337
        else:
            catId = data[0]

        return int(catId)

    def save(self, item):
        '''
        数据保存到45服务器的mongodb中
        :param item:
        :return:
        '''
        res = self.collection.find_one(
            {"liveId": item.get('liveId'), "itemId": item.get('itemId')})

        if not res:
            categoryid = self.select_goods_categoryId(int(item.get('categoryId')))
            data = {
                'anchorId': item.get('accountId'),
                'anchorName': item.get('accountName'),
                'title': item.get('title'),
                'createTime': item.get('createTime'),
                'itemId': item.get('itemId'),
                'sellerId': item.get('sellerId'),
                'goods_url': item.get('goods_url'),
                'shopName': item.get('shopName'),
                'liveId': item.get('liveId'),
                'liveURL': item.get('liveURL'),
                'livePrice': item.get('livePrice'),
                'categoryId': item.get('categoryId'),
                'class2name': item.get('class2name'),
                'shopId': item.get('shopId'),
                'shopType': item.get('shopType'),
                'maintype': item.get('maintype'),
                'rootCategoryId': item.get('rootCategoryId'),
                "Monthly_payment": None,
                "CommtentCount": None,
                'is_dispose': 1,  # 默认数据未处理
                'plcategory': categoryid  # 此字段对应的pl的category字段不全
            }

            self.collection.insert_one(data)
            self.r.sadd('liveId:ItemId', '{}:{}'.format(item.get('liveId'), item.get('itemId')))

    def get_data(self):
        '''requests请求zhiboshuju.com服务器获取json数据'''
        while 1:
            result = self.r.spop('anchorId')  # db = 1 上的anchorid
            if result:
                print(result.decode('utf-8').split(':')[0])
                postdata = {
                    'accountId': str(result.decode('utf-8').split(':')[0]),
                    'openId': 'ofYto04ZtE57zTesjffxdeWmZzQQ',
                    'page': '1',
                    'limit': '1000',
                    'rootCategoryId': ''  # 此字段有问题，返回数据不全
                }
                try:
                    response = requests.post(url='https://www.zhiboshuju.com/shopanchorWeChat/selectaccountsevendate', data=postdata).json()
                except:
                    self._close_mysql_conn()
                    break

                json_obj = response.get('data')
                if json_obj:
                    anchorspiderItem = {}
                    for data in json_obj:
                        anchorspiderItem['accountId'] = data['accountId']  # 主播ID
                        anchorspiderItem['accountName'] = data['accountName']  # 主播昵称
                        anchorspiderItem['title'] = data['title']  # 商品标题
                        anchorspiderItem['createTime'] = data['createTime']  # 商品上架时间
                        anchorspiderItem['itemId'] = data['itemId']  # 商品ID
                        anchorspiderItem['sellerId'] = data['sellerId']  # 商品售卖ID
                        anchorspiderItem['goods_url'] = 'https://detail.tmall.com/item.htm?id=' + data['itemId']
                        anchorspiderItem['shopName'] = data['shopName']  # 商店名称
                        anchorspiderItem['liveId'] = data['liveId']  # 直播间ID
                        anchorspiderItem['liveURL'] = 'http://huodong.m.taobao.com/act/talent/live.html?id=%s' % data['liveId']  # 直播间URL
                        anchorspiderItem['livePrice'] = data['livePrice']  # 商品直播时的价格
                        anchorspiderItem['categoryId'] = data['categoryId']  # 商品分类ID
                        anchorspiderItem['class2name'] = data['class2name']  # 商品所属类别
                        anchorspiderItem['shopId'] = data['shopId']  # 商店ID
                        anchorspiderItem['shopType'] = data['shopType']  # 商店级别
                        anchorspiderItem['maintype'] = data['maintype']  # 商品主分类
                        anchorspiderItem['rootCategoryId'] = data['rootCategoryId']  #
                        try:
                            self.save(anchorspiderItem)
                        except:
                            self._close_mysql_conn()
                            break
                else:
                    self.r.sadd('anchorId_noData', result.decode('utf-8').split(':')[0])
            else:
                self._close_mysql_conn()
                break

    def run(self):
        pass


if __name__ == '__main__':
    gs = GoodsSpider(env='dev')
    gs.get_data()

