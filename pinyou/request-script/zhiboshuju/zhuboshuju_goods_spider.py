import time
import redis
import requests
from pymongo import MongoClient
from config import environments
import pymysql
from logs.wirte_logs import Logger


class GoodsSpider(object):

    def __init__(self, env):
        self.env_dict = environments.get(env)
        self.r = redis.StrictRedis().from_url(url=self.env_dict.get('redis_url'))
        self.callback_url = environments.get(env).get('callback_url')
        self.client = MongoClient(self.env_dict.get('mongodb_host'), port=self.env_dict.get('mongodb_port'))
        self.db = self.client['pltaobao']
        self.collection = self.db['goods_detail']

    def select_goods_categoryId(self, catId):

        db = pymysql.connect(host=self.env_dict.get('mysql_host'),  # 数据库服务器IP
                             port=self.env_dict.get('mysql_port'),
                             user=self.env_dict.get('mysql_user'),
                             passwd=self.env_dict.get('mysql_pwd'),
                             db=self.env_dict.get('db'))  # 数据库名称

        # 使用cursor()方法创建一个游标对象cur
        cur = db.cursor()

        # 使用execute()执行SQL语句
        cur.execute("select category from pl_taobao_category where tao_leaf_category_id={}".format(catId))

        # 使用 fetchone() 方法获取一条数据
        data = cur.fetchone()
        if not data:
            catId = 2337
        else:
            catId = data[0]
        # 关闭数据库连接
        db.close()
        return int(catId)

    def save(self, item):
        res = self.collection.find_one(
            {"liveId": str(item.get('liveId')), "itemId": str(item.get('itemId'))})
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
                'is_dispose': 2,
                'plcategory': categoryid
            }

            self.collection.insert_one(data)
            # self.r.sadd('liveId:ItemId', '{}:{}'.format(item.get('liveId'), item.get('itemId')))

    def check_task(self, anchorId):
        res = self.collection.find_one({"anchorId": str(anchorId)})
        if res:
            return 1
        return 0

    def get_data(self):

        while 1:
            result = self.r.spop('anchorId:anchorName:uid:roomId')
            if result:
                self.anchorId = result.decode('utf-8').split(':')[0]
                self.uid = result.decode('utf-8').split(':')[2]
                self.anchorName = result.decode('utf-8').split(':')[1]
                self.roomId = result.decode('utf-8').split(':')[3]
                flag = self.check_task(self.anchorId)
                if flag:
                    self.r.sadd('finish_anchorId:status:uid:anchorName:roomId:is_repetition', "{}:{}:{}:{}:{}:{}".format(self.anchorId, 1, self.uid, self.anchorName, self.roomId, 1))
                    self.send_sign(1)
                    continue
                self.send_sign(1)
                postdata = {
                    'accountId': str(self.anchorId),
                    'openId': 'ofYto04ZtE57zTesjffxdeWmZzQQ',
                    'page': '1',
                    'limit': '1000',
                    'rootCategoryId': ''
                }
                response = requests.post(url='https://www.zhiboshuju.com/shopanchorWeChat/selectaccountsevendate', data=postdata).json()

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
                        self.save(anchorspiderItem)
                    Logger('zhuboshuju_goods_spider.log', level='info').logger.info(f'此主播数据已经爬完：{self.anchorId}:{self.anchorName}，待交电商记爬虫')
                    self.r.sadd('finish_anchorId:status:uid:anchorName:roomId:is_repetition',"{}:{}:{}:{}:{}:{}".format(self.anchorId, 1, self.uid, self.anchorName, self.roomId, 0))
                else:
                    Logger('zhuboshuju_goods_spider.log', level='info').logger.info(f'此主播暂无数据：{self.anchorId}:{self.anchorName}')
                    self.r.sadd('finish_anchorId:status:uid:anchorName:roomId:is_repetition',"{}:{}:{}:{}:{}:{}".format(self.anchorId, 1, self.uid, self.anchorName, self.roomId, 0))
                    self.send_sign(3)

    def run(self):
        pass

    def send_sign(self, num):
        requests.post(url=self.callback_url, data={"uid": int(self.uid), 'anchorState': num, 'anchorName': self.anchorName, 'roomId': self.roomId})
        pass


if __name__ == '__main__':
    gs = GoodsSpider(env='pro')
    gs.get_data()

