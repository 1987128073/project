import json
import re
import time
from pymongo import MongoClient
from config import environments


class SaveData(object):

    def __init__(self, env):
        self.env_dict = environments.get(env)
        self.flag = self.env_dict.get('flag')
        self.client = MongoClient(self.env_dict.get('mongodb_host'), self.env_dict.get('mongodb_port'))
        self.db = self.client['pc_data_origin']

    def json_loads(self, text):
        pattern = re.compile(r'mtopjsonp\d\(([\s\S].*)\)', re.S)
        a = re.search(pattern, text).group(1)
        return a

    def save_anchor_info(self, data):
        # print(data)

        try:
            anchor_info_list = data.get('searchDatas')[0].get('liveSearchInfos')
        except:
            return

        for anchor_info in anchor_info_list:
            anchor_id = anchor_info.get('accountId')
            anchor_name = anchor_info.get('accountName')
            fans_count = anchor_info.get('fansNum')
            headImg = anchor_info.get('headImg')
            sub_type = anchor_info.get('subType')

            res = self.client['pltaobao']['anchor_info'].find_one({'_id': int(anchor_id)})
            if not res:
                data = {

                    'anchorId': str(anchor_id),
                    'anchorName': anchor_name,
                    'houseId': None,
                    'fansCount': int(fans_count),
                    'liveCount': None,
                    'city': None,
                    'creatorType': sub_type,
                    'darenScore': None,
                    'descText': None,
                    'anchorPhoto': headImg,
                    'organId': None,
                    'fansFeature': None,
                    'historyData': None,
                }
                self.client['pltaobao']['anchor_info'].insert_one(data)

            # res2 = self.client['v3_app_data_parsed']['anchors'].find_one({'_id': int(anchor_id)})
            # if not res2:
            #     data = {
            #         '_id': int(anchor_id),
            #         'room_num': None,
            #         'nick': anchor_name,
            #         'organ_id': None,
            #         'anchor_type': sub_type,
            #         'head_image': headImg,
            #         'create_at': int(time.time()),
            #         'head_background_image': None,
            #         'have_into_sql': False
            #     }
            #     self.client['v3_app_data_parsed']['anchors'].insert_one(data)

    def save_itemlist(self, data, json_obj):
        a = self.json_loads(data)
        # print(a)
        itemlist = self.db['itemlist'] if self.flag else self.db['itemlist_pro']

        anchorId = json_obj.get('creatorId')
        liveId = json_obj.get('liveId')
        print(anchorId, liveId)
        res = itemlist.find_one({"_id": "{}:{}".format(anchorId, liveId)})
        if not res:
            data = {
                "_id": "{}:{}".format(anchorId, liveId),
                "itemList": json.loads(a).get('data').get('itemList'),
                "create_time": time.strftime("%Y-%m-%d", time.localtime()),
                "update_time": time.strftime("%Y-%m-%d", time.localtime()),
                "is_parsed": False
            }
            itemlist.insert_one(data)
        pass

    def save_livedetail(self, data, liveId):
        livedetail = self.db['livedetail'] if self.flag else self.db['livedetail_pro']
        a = self.json_loads(data)
        # print(a)
        json_obj = json.loads(a).get("data")
        res = livedetail.find_one({"_id": "{}:{}".format(json_obj.get("broadCaster").get('accountId'), liveId)})
        if not res:
            data = {
                "_id": "{}:{}".format(json_obj.get("broadCaster").get('accountId'), liveId),
                "livedetail": json_obj,
                "create_time": time.strftime("%Y-%m-%d", time.localtime()),
                "update_time": time.strftime("%Y-%m-%d", time.localtime()),
                "is_parsed": False
            }
            livedetail.insert_one(data)
        pass

    def save_feedsdetail(self, data):
        feedsdetail = self.db['feedsdetail'] if self.flag else self.db['feedsdetail_pro']
        a = self.json_loads(data)
        # print(a)
        json_obj = json.loads(a).get("data").get('result')

        if json_obj:
            try:
                feed_list = json_obj.get('data')[-1].get('co').get('result').get('data').get('feeds')
            except:
                feed_list = []
            if feed_list:
                l = []
                anchor_id = ''
                for i in feed_list:

                    if i.get("owner") != 'taolive':
                        continue
                    anchor_id = i.get('userId')
                    l.append(i)
                res = feedsdetail.find_one({"_id": "{}".format(int(str(time.time()).split('.')[0]))})

                if not res:
                    data = {
                        "_id": "{}".format(int(str(time.time()).split('.')[0])),
                        'anchor_id': anchor_id,
                        "feed_detail": l,
                        "create_time": time.strftime("%Y-%m-%d", time.localtime()),
                        "update_time": time.strftime("%Y-%m-%d", time.localtime()),
                        "is_parsed": False
                    }
                    feedsdetail.insert_one(data)
                    del l

    def item_info(self, item_id, data):
        item_info = self.db['item_info'] if self.flag else self.db['item_info_pro']
        a = self.json_loads(data)
        json_obj = json.loads(a).get("data")
        res = item_info.find_one({"_id": "{}".format(item_id)})
        if not res:
            data = {
                "_id": "{}".format(item_id),
                "item_info": json_obj,
                "create_time": time.strftime("%Y-%m-%d", time.localtime()),
                "update_time": time.strftime("%Y-%m-%d", time.localtime()),
                "is_parsed": False
            }
            item_info.insert_one(data)