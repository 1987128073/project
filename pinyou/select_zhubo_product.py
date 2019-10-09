import time

from pymongo import MongoClient


def timestamp_to_timestr(timeStamp):
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


def a(name):
    client = MongoClient('192.168.1.180', port=32766)
    db = client['v3_app_data_parsed']
    anchor = db['anchors'].find_one({'nick': name})
    anchor_id = anchor.get('_id')
    live_id_list = db['lives'].find({'anchor_id': anchor_id})
    exist_live = []
    for live in live_id_list:

        res = db['live_monitoring'].find_one({'_id': live.get('_id')})
        if res:
            exist_live.append(live.get('_id'))

    if exist_live is None:
        print('该主播暂未直播')
        return

    for live_id in exist_live:
        item_id = []
        res = db['product_lives'].find({"live_id": live_id})
        if res:
            for data in res:
                item_id.append(data.get('product_id'))
                item_list = db['product_variables'].find({'item_id': data.get('product_id')})
                l = []
                for item in item_list:
                    l.append(item)
                if l:
                    print(f'主播名为：{name}({anchor_id})带货商品id({data.get("product_id")})在场次id为：{live_id}销量为：{l[-1].get("sold_count") - l[0].get("sold_count")}')
                # for index, item in enumerate(item_list):
                #     print(f'主播{name}({anchor_id})带货商品id({data.get("product_id")})在{timestamp_to_timestr(item.get("created_at"))}时间月销量为：{item.get("sold_count")}')


if __name__ == '__main__':
    a('欢欢PL哒')


