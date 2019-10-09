from pymongo import MongoClient


def insert_m():
    client = MongoClient(host='192.168.1.51')
    db = client['pltaobao']
    collection01 = db['tb_anchor_goods']
    collection02 = db['2019-08-13tb_anchor_goods']
    for i in collection01.find({}):
        res = collection02.find_one({"accountId": i.get('accountId'), 'createTime':i.get('createTime'), "itemId": i.get('itemId')})
        if not res:
            anchor = dict()
            anchor['accountId'] = i.get('accountId')
            anchor['accountName'] = i.get('accountName')
            anchor['title'] = i.get('title')
            anchor['createTime'] = i.get('createTime')
            anchor['itemId'] = i.get('itemId')
            anchor['sellerId'] = i.get('sellerId')
            anchor['goods_url'] = i.get('goods_url')
            anchor['shopName'] = i.get('shopName')
            anchor['liveId'] = i.get('liveId')
            anchor['liveURL'] = i.get('liveURL')
            anchor['livePrice'] = i.get('livePrice')
            anchor['categoryId'] = i.get('categoryId')
            anchor['class2name'] = i.get('class2name')
            anchor['shopId'] = i.get('shopId')
            anchor['shopType'] = i.get('shopType')
            anchor['maintype'] = i.get('maintype')
            anchor['rootCategoryId'] = i.get('rootCategoryId')
            collection01.insert_one(anchor)

def updata_m():
    client = MongoClient(host='192.168.1.51')
    db = client['pltaobao']
    collection01 = db['tb_anchor_goods']
    collection02 = db['2019-08-13tb_anchor_goods']
    for i in collection01.find({}):
        res = collection02.find_one(
            {"accountId": i.get('accountId'), 'createTime': i.get('createTime'), "itemId": i.get('itemId')})
        if not res:
            anchor = dict()
            anchor['accountId'] = i.get('accountId')
            anchor['accountName'] = i.get('accountName')
            anchor['title'] = i.get('title')
            anchor['createTime'] = i.get('createTime')
            anchor['itemId'] = i.get('itemId')
            anchor['sellerId'] = i.get('sellerId')
            anchor['goods_url'] = i.get('goods_url')
            anchor['shopName'] = i.get('shopName')
            anchor['liveId'] = i.get('liveId')
            anchor['liveURL'] = i.get('liveURL')
            anchor['livePrice'] = i.get('livePrice')
            anchor['categoryId'] = i.get('categoryId')
            anchor['class2name'] = i.get('class2name')
            anchor['shopId'] = i.get('shopId')
            anchor['shopType'] = i.get('shopType')
            anchor['maintype'] = i.get('maintype')
            anchor['rootCategoryId'] = i.get('rootCategoryId')
            collection01.insert_one(anchor)


if __name__ == '__main__':
    insert_m()