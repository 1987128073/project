import json

from pymongo import MongoClient

from save_data import SaveData

client = MongoClient('192.168.1.180', port=32766)
origin_db = client['v3_app_data_origin']
parsed_db = client['v3_app_data_parsed']

item_list = origin_db['item_list']
product_lives = parsed_db['product_lives']

sd = SaveData('dev')

all_data = item_list.find({})
n = 1
for data in all_data:
    json_obj = sd.json_loads(data.get('data'))
    print(n)
    for i in json.loads(json_obj).get("data").get('itemList'):
        goodsIndex = int(i.get('goodsIndex'))
        item_id = int(i.get('goodsList')[0].get('itemId'))
        try:
            live_id = int(i.get('goodsList')[0].get('extendVal').get('liveId'))
        except:
            break
        product_lives.update_one({'_id': f'{item_id}:{live_id}'}, {'$set': {"good_index": goodsIndex}})
    n += 1


