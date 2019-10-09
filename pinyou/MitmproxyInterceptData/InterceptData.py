# -*- coding: utf-8 -*-
import base64
import json

import mitmproxy.http
from mitmproxy import ctx
from pymongo import MongoClient


class Counter:

    def __init__(self):
        pass

    #设置上游代理
    def request(self, flow: mitmproxy.http.HTTPFlow):
         if flow.request.method == "CONNECT":
             return

    def response(self, flow: mitmproxy.http.HTTPFlow):
        self.client = MongoClient('192.168.1.45')
        self.db = self.client['pltaobao']
        self.collection = self.db['TBCategory']
        # 拦截包的信息
        if 'https://router.publish.taobao.com/router/asyncOpt.htm?optType=categorySelectChildren' == flow.request.url:
            print(flow.response.text)
            json_obj = json.loads(flow.response.text).get('data').get('dataSource')
            for data in json_obj:
                groupId = data.get('groupId')
                name = data.get('groupName')

                res = self.collection.find_one({'_id': groupId})
                if not res:
                    data1={
                        '_id': groupId,
                        'name': name,
                        'parentId': None
                    }
                    self.collection.insert_one(data1)

                for children in data.get('children'):
                    childrenid = children.get('id')
                    childrenidname = children.get('name')
                    parentId = groupId
                    res = self.collection.find_one({'_id': childrenid})
                    if not res:
                        data = {
                            '_id': childrenid,
                            'name': childrenidname,
                            'parentId': parentId
                        }
                        self.collection.insert_one(data)


        if 'https://router.publish.taobao.com/router/asyncOpt.htm?optType=categorySelectChildren&catId=' in flow.request.url:
            json_obj = json.loads(flow.response.text).get('data').get('dataSource')
            for data in json_obj:
                if not data.get('leaf'):
                    id = data.get('id')
                    name = data.get('name')
                    parentId = data.get('idpath')[-2]
                    res = self.collection.find_one({'_id': id})
                    if not res:
                        data = {
                            '_id': id,
                            'name': name,
                            'parentId': parentId
                        }
                        self.collection.insert_one(data)

        if 'https://router.publish.taobao.com/router/asyncOpt.htm?optType=taobaoBrandSelectQuery&queryType=more&catId=' in flow.request.url:
            json_obj = json.loads(flow.response.text).get('data').get('dataSource')
            for data in json_obj:
                if not data.get('leaf'):
                    id = data.get('id')
                    name = data.get('name')
                    parentId = data.get('idpath')[-2]
                    res = self.collection.find_one({'_id': id})
                    if not res:
                        data = {
                            '_id': id,
                            'name': name,
                            'parentId': parentId
                        }
                        self.collection.insert_one(data)

        if 'https://acs.m.taobao.com/gw/mtop.taobao.iliad.comment.query.latest/1.0/?' in flow.request.url:
            print(flow.response.text)

        if 'http://h5api.m.taobao.com/h5/mtop.mediaplatform.video.livedetail.itemlist/1.0/?jsv=2.4.0&appKey=12574478&' in flow.request.url:
            if len(flow.response.text) > 140:
                json_obj = json.loads(flow.request.query.get('data'))
                anchorId = json_obj.get('creatorId')
                liveId = json_obj.get('liveId')
                print(flow.response.text)
                # print(flow.response.text)
            # json_obj = json.loads(flow.response.text).get('data')
            # with open("record.json", "w") as f:
            #     json.dump(json_obj, f)



addons = [
    Counter()
]