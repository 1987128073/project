import redis
from pymongo import MongoClient
from config import environments
from tmall_spider import TmallSpider
from utils.time_change import get_today_zero_timestamp


class ParseData(object):

    def __init__(self, env):
        self.env_dict = environments.get(env)
        self.flag = self.env_dict.get('flag')
        self.r = redis.StrictRedis().from_url(url=self.env_dict.get('redis_url'))
        self.mongodb_url = self.env_dict.get('mongodb_url')
        self.origin_db_name = 'pc_data_origin'
        if self.flag:
            self.feedsdetail = 'feedsdetail'
            self.itemlist = 'itemlist'
            self.livedetail = 'livedetail'
            self.save_db_name = 'pl_taobao_dataV3'
        else:
            self.save_db_name = 'v3_app_data_parsed'
            self.feedsdetail = 'feedsdetail_pro'
            self.itemlist = 'itemlist_pro'
            self.livedetail = 'livedetail_pro'

        self.client = MongoClient(host=self.env_dict.get('mongodb_host'), port=self.env_dict.get('mongodb_port'))
        self.origin_db = self.client[self.origin_db_name]
        self.save_db = self.client[self.save_db_name]
        self.TM = TmallSpider()

    def parse_feedsdetail(self):
        collection = self.origin_db[self.feedsdetail]
        while 1:
            if collection.find_one({'is_parsed': False}) is None:
                continue

            res = collection.find({'is_parsed': False}, no_cursor_timeout=True)

            for result in res:
                _id = result.get('_id')
                data = result.get('feed_detail')

                anchorId = result.get('anchor_id')
                for i in data:
                    if 'living' not in i.get('url'):
                        liveId = i.get('feedId')
                        self.r.sadd('anchorId:liveId', f'{anchorId}:{liveId}')
                    else:
                        # push_task('living', 'living', f'{data.get("_id")}')
                        pass
                collection.update_one({"_id": _id}, {'$set': {'is_parsed': True}})
            res.close()

    def parse_itemlist(self):
        collection = self.origin_db[self.itemlist]

        while 1:
            if collection.find_one({'is_parsed': False}) is None:
                continue

            res = collection.find({'is_parsed': False}, no_cursor_timeout=True, batch_size=5)

            for data in res:
                _id = data.get('_id')
                itemList = data.get('itemList')
                anchor_id = int(_id.split(':')[0])
                liveId = int(_id.split(':')[1])
                for i in itemList:
                    item_id = int(i.get('goodsList')[0].get('itemId'))

                    categoryId, rootCatId, shopId, shop_name, buy_enable, flag = self.TM.getid(item_id)

                    if flag == 1:
                        print('ip被禁用')
                        continue
                    top_leaf_categoryid = categoryId
                    top_leaf_categoryname = None
                    root_categoryid = rootCatId
                    root_categoryname = None
                    brand_name = None
                    brand_id = None
                    comment_count = None
                    fav_count = None
                    shop_id = shopId
                    shop_name = shop_name
                    shop_type = None
                    shelf_time = None
                    live_shelf_time = None
                    nomal_price = None

                    # live_pro_anchor table
                    live_pro_anchor = self.save_db['live_pro_anchor'].find_one({'_id': item_id})
                    if not live_pro_anchor:
                        data = {
                            '_id': item_id,  # 商品id
                            'live_id': liveId,
                            'anchor_id': anchor_id,
                            'item_title': i.get('goodsList')[0].get('itemName'),
                            'item_images': i.get('goodsList')[0].get('itemPic'),
                            'item_url': i.get('goodsList')[0].get('itemUrl'),
                            'buy_enable': buy_enable,
                            'item_subtitle': None,
                            'live_price': float(i.get('goodsList')[0].get('itemPrice')),
                            'top_leaf_categoryid': top_leaf_categoryid,
                            'top_leaf_categoryname': top_leaf_categoryname,
                            'root_categoryid': root_categoryid,
                            'root_categoryname': root_categoryname,
                            'brand_name': brand_name,
                            'brand_id': brand_id,
                            'comment_count': comment_count,
                            'fav_count': fav_count,
                            'shop_id': shop_id,
                            'shop_name': shop_name,
                            'shop_type': shop_type,
                            'shelf_time': shelf_time,
                            'live_shelf_time': live_shelf_time,
                            'nomal_price': nomal_price

                        }
                        self.save_db['live_pro_anchor'].insert_one(data)

                collection.update_one({"_id": _id}, {'$set': {'is_parsed': True}})
            res.close()

    def parse_livedetail(self):
        collection = self.origin_db[self.livedetail]
        while 1:
            if collection.find_one({'is_parsed': False}) is None:
                continue

            res = collection.find({'is_parsed': False}, no_cursor_timeout=True, batch_size=5)

            for result in res:
                _id = result.get('_id')

                #  live_variables table
                liveId = int(result.get('livedetail').get('liveId'))
                # liveId 有可能为零，无法匹配
                if liveId == 0:
                    collection.update_one({"_id": _id}, {'$set': {'is_parsed': True}})
                    continue
                anchor_id = int(result.get('livedetail').get('accountId'))

                # anchor_id 有可能为零，无法匹配
                if anchor_id == 0:
                    collection.update_one({"_id": _id}, {'$set': {'is_parsed': True}})
                    continue

                live_time = int(result.get('livedetail').get('startTime'))/1000  # 转换为当时直播的0点时间戳

                live_variables = self.save_db['live_variables'].find_one({'_id': liveId})

                if not live_variables:
                    data = {
                        'live_id': liveId,
                        'anchor_id': anchor_id,
                        'view_count': int(result.get('livedetail').get('viewCount')),
                        'total_join_count': int(result.get('livedetail').get('totalJoinCount')),
                        'created_at': int(live_time),  # 时间戳
                    }
                    self.save_db['live_variables'].insert_one(data)

                #  anchor_variables table
                zero_point = get_today_zero_timestamp(live_time)
                fansNum = int(result.get('livedetail').get('broadCaster').get('fansNum'))
                anchor_variables = self.save_db['anchor_variables'].find_one({'_id': f'{result.get("livedetail").get("accountId")}:{zero_point}'})
                if not anchor_variables:
                    data = {
                        '_id': f'{anchor_id}:{zero_point}',
                        'fans_count': fansNum,
                        'live_count': None,
                        'created_at': int(live_time),  # 时间戳
                    }

                    self.save_db['anchor_variables'].insert_one(data)

                # anchors table
                anchors = self.save_db['anchors'].find_one(
                    {'_id': int(result.get("livedetail").get("accountId"))})
                if not anchors:
                    data = {
                        '_id': anchor_id,
                        'nick': result.get('livedetail').get('broadCaster').get('accountName'),
                        'room_num': int(result.get('livedetail').get('broadCaster').get('roomNum')),
                        'anchor_type': result.get('livedetail').get('broadCaster').get('type'),
                        'head_image': result.get('livedetail').get('broadCaster').get('headImg'),
                        'head_background_image': result.get('livedetail').get('broadCaster').get('backGroundImg'),
                        'have_into_sql': False
                    }
                    self.save_db['anchors'].insert_one(data)

                collection.update_one({"_id": _id}, {'$set': {'is_parsed': True}})
            res.close()


if __name__ == '__main__':
    pd = ParseData('dev')
    pd.parse_feedsdetail()
