import base64
import json
import time
import js2py
import requests
from requests.auth import HTTPProxyAuth


def e():
    context = js2py.EvalJs()
    with open('tbjs.js', 'r') as f:
        context.execute(f.read())
    time_ = int(time.time()*1000)
    # print(time_)
    sign3 = context.sign('17e1d865441fae196a36bc8316c7e05e', str(time_), '12574478', {"type":"0","liveId":"233832148449","creatorId":"165229494"})
    # sign1 = context.sign('3987a097cd011707974a8addc09ba787', time_, "12574478", {})
    proxies = {
        'http': 'http://http-proxy-t1.dobel.cn:9180'
    }
    auth = HTTPProxyAuth('ATLANDG4EGPK5S0', 'LKHN5uFx')

    headers2 = {
        'Referer': 'http://huodong.m.taobao.com/act/talent/live.html?id=232537510437',
        # 'Sec-Fetch-Mode': 'no-cors',
        'cookie':'t=c18e36d616338aa7822c58ab46a1388e; _m_h5_tk=17e1d865441fae196a36bc8316c7e05e_1566879424629; _m_h5_tk_enc=51e9d2d26b6c35b9ccff88b7e344bc58; cna=7nPrFc4BfSQCATolAucPFfH1; cookie2=188bebd4a54d6cd0f0a0f9bdae3733e8; _tb_token_=e663ebee53d3e; l=cBLRsl7qqJOKT3RtBOCNCuI8LA79sIRAguPRwCVvi_5IL6L_V__OkuKGYFp6cjWd9YTB4aVvW6J9-etkiegNY-Qu-yLF.; isg=BD09yfV2PDhknZhU6t3oHbeATJn3cnBVsfkCbf-CexTDNl1oxyri_ATk5CrVtonk',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    }
    params2 = {
        "jsv": "2.4.0",
        "appKey": 12574478,
        "t": str(time_),
        "sign": sign3,
        "AntiCreep": "true",
        "api": "mtop.mediaplatform.video.livedetail.itemlist",
        "v": "1.0",
        "type": "jsonp",
        "dataType": "jsonp",
        "timeout": '20000',
        "callback": "mtopjsonp4",
        "data": '{"type":"0","liveId":"233832148449","creatorId":"165229494"}',
    }
    s = requests.Session()
    response = s.get(url='https://h5api.m.tmall.com/h5/mtop.mediaplatform.live.item.pre.get/2.0/?', headers=headers2, params=params2)
    print(response.content.decode('utf-8'))

def f():
    context = js2py.EvalJs()
    with open('tbjs.js', 'r') as f:
        context.execute(f.read())
    time_ = int(time.time() * 1000)
    print(time_)
    sign = context.sign('b8f27656f01f19a8bcabe40bbd86a8b6', '1566611055965', '12574478', {"type":"0","liveId":"232537510437","creatorId":"2123374022"})
    print(sign)


if __name__ == '__main__':
    e()
    # f()