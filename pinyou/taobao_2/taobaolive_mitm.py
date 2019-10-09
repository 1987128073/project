# -*- coding: utf-8 -*-
import json, re

import mitmproxy.http
from mitmproxy import ctx
from pymongo import MongoClient
import time


class Counter:

    def __init__(self):
        pass

    def _json_loads(self, text):
        pattern = re.compile(r' mtopjsonp\d\(([\s\S].*)\)', re.S)
        a = re.search(pattern, text).group(1)
        return a

    # 设置上游代理
    def request(self, flow: mitmproxy.http.HTTPFlow):
        if flow.request.method == "CONNECT":
            return

    def response(self, flow: mitmproxy.http.HTTPFlow):

        client = MongoClient('192.168.1.180', port=32766)
        db = client['pc_data_origin']
        collection1 = db['livedetail_test']
        collection2 = db['itemlist_test']
        # 拦截包的信息

        if 'http://h5api.m.taobao.com/h5/mtop.mediaplatform.video.livedetail.itemlist' in flow.request.url:
            if len(flow.response.text) > 140:
                a = self._json_loads(flow.response.text)
                # print(a)
                json_obj = json.loads(flow.request.query.get('data'))
                anchorId = json_obj.get('creatorId')
                liveId = json_obj.get('liveId')
                res = collection2.find_one({"_id": "{}:{}".format(anchorId, liveId)})
                if not res:
                    data = {
                        "_id": "{}:{}".format(anchorId, liveId),
                        "itemList": json.loads(a).get('data').get('itemList'),
                        "create_time": time.strftime("%Y-%m-%d", time.localtime()),
                        "update_time": time.strftime("%Y-%m-%d", time.localtime()),
                        "is_parsed": False
                    }
                    collection2.insert_one(data)
                # else:
                #     if str(res.get("update_time")) != str(time.strftime("%Y-%m-%d", time.localtime())):
                #         collection2.update_one(
                #             {'_id': "{}:{}".format(anchorId, liveId)},
                #             {"$set":
                #                 {
                #                     "itemList": json.loads(flow.response.text).get('data').get('itemList'),
                #                     "update_time": time.strftime("%Y-%m-%d", time.localtime()),
                #                     "is_parsed": False
                #                 }
                #             }
                #         )

        if 'http://h5api.m.taobao.com/h5/mtop.mediaplatform.live.livedetail' in flow.request.url:
            if len(flow.response.text) > 140:
                a = self._json_loads(flow.response.text)
                # print(a)
                liveId = json.loads(flow.request.query.get('data')).get('liveId')
                json_obj = json.loads(a).get("data")
                res = collection1.find_one({"_id": "{}:{}".format(json_obj.get("broadCaster").get('accountId'), liveId)})
                if not res:
                    data = {
                        "_id":  "{}:{}".format(json_obj.get("broadCaster").get('accountId'), liveId),
                        "livedetail": json_obj,
                        "create_time": time.strftime("%Y-%m-%d", time.localtime()),
                        "update_time": time.strftime("%Y-%m-%d", time.localtime()),
                        "is_parsed": False
                    }
                    collection1.insert_one(data)

                # else:
                #     if str(res.get("update_time")) != str(time.strftime("%Y-%m-%d", time.localtime())):
                #         collection1.update_one(
                #             {'_id': "{}".format(json_obj.get("accountId"))},
                #             {"$set":
                #                 {
                #                     "livedetail": json_obj,
                #                     "update_time": time.strftime("%Y-%m-%d", time.localtime()),
                #                     "is_parsed": False
                #                 }
                #             }
                #         )


addons = [
    Counter()
]
