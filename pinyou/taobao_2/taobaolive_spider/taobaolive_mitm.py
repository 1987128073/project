# -*- coding: utf-8 -*-
import json
import mitmproxy.http
from mitmproxy import ctx

from save_data import SaveData


class Counter:

    def __init__(self):
        self.save_data = SaveData(env='dev')
        pass

    # 设置上游代理
    def request(self, flow: mitmproxy.http.HTTPFlow):
        if flow.request.method == "CONNECT":
            return

    def response(self, flow: mitmproxy.http.HTTPFlow):
        # 拦截包的信息
        if 'http://h5api.m.taobao.com/h5/mtop.mediaplatform.video.livedetail.itemlist' in flow.request.url:
            if len(flow.response.text) > 140:
                json_obj = json.loads(flow.request.query.get('data'))
                self.save_data.save_itemlist(flow.response.text, json_obj)

        if 'https://h5api.m.taobao.com/h5/mtop.taobao.maserati.xplan.render/' in flow.request.url:
            if len(flow.response.text) > 145:
                # anchorId = json.loads(flow.request.query.get('data')).get('accountId')
                self.save_data.save_feedsdetail(flow.response.text)

        if 'http://h5api.m.taobao.com/h5/mtop.mediaplatform.live.livedetail' in flow.request.url:
            if len(flow.response.text) > 140:
                liveId = json.loads(flow.request.query.get('data')).get('liveId')
                self.save_data.save_livedetail(flow.response.text, liveId)

        if 'https://acs.m.taobao.com/gw/mtop.mediaplatform.live.searchv2' in flow.request.url:
            if len(flow.response.text) > 140:
                json_obj = json.loads(flow.response.text).get('data')
                self.save_data.save_anchor_info(json_obj)

        if 'https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail' in flow.request.url:
            if len(flow.response.text) > 140:
                item_id = json.loads(flow.request.query.get('data')).get('id')
                self.save_data.item_info(item_id, flow.response.text)


addons = [
    Counter()
]
