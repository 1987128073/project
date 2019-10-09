import requests
# headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.162 Safari/537.36',
#         }
# num = 0
# while 1:
#     num += 1
#     response = requests.get(url='https://h5api.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?api=mtop.taobao.detail.getdetail&v=6.0&isSec=0&ecode=0&AntiFlood=true&AntiCreep=true&H5Request=true&ttid=2018%40taobao_h5_9.9.9&type=jsonp&dataType=jsonp&callback=mtopjsonp1&data=%7B%22id%22%3A%22601993310690%22%2C%22ali_refid%22%3A%22a3_430673_1006%3A1125501630%3AN%3ArvrUsViJQFAUL6P%2BVfgyjg%3D%3D%3Ac7d8f4e1f94c2da5c11f45e0b85032d5%22%2C%22ali_trackid%22%3A%221_c7d8f4e1f94c2da5c11f45e0b85032d5%22%2C%22spm%22%3A%22a2e15.8261149.07626516002.1%22%2C%22itemNumId%22%3A%22601993310690%22%2C%22itemId%22%3A%22601993310690%22%2C%22exParams%22%3A%22%7B%5C%22id%5C%22%3A%5C%22601993310690%5C%22%2C%5C%22', headers=headers)
#     if response.status_code != 200:
#         print(num)
#         break
# response = requests.get(url='https://detail.tmall.com/item.htm?id=9618854849', headers=headers, timeout=5)
# if 'deny cc' in response.text:
#     response = requests.get(url='https://detail.tmall.com/item.htm?id=9618854849', headers=headers, timeout=5)
# if response.status_code == 200:
#     print(response.url)
#     cid_pattern = re.compile(r',categoryId:(\d*?),', re.S)
#     rcid_pattern = re.compile(r'name="rootCatId" value="(\d*?)"', re.S)
#     shopId_pattern = re.compile(r"; shopId=(\d*?);", re.S)
#     shop_name_pattern = re.compile(r'sellerNickName:"(.*?)",', re.S)
#     brand_name = re.compile(r'"brand":"(.*?)",', re.S)
#     brand_id = re.compile(r',"brandId":"(.*?)",', re.S)
#
#     #
#     # cid_pattern = re.compile(r" cid\s*: '(\d*?)'", re.S)
#     # rcid_pattern = re.compile(r"rcid\s*: '(\d*?)'", re.S)
#     # shopId_pattern = re.compile(r" shopId\s*: '(\d*?)'", re.S)
#     # shop_name_pattern = re.compile(r" shopName\s*: '(.*?)'", re.S)
#     # status_pattern = re.compile(r" status\s*: (.*?),", re.S)
#     #
#     try:
#         categoryId = int(re.search(cid_pattern, response.text).group(1))
#     except:
#         categoryId = None
#     try:
#         rootCatId = int(re.search(rcid_pattern, response.text).group(1))
#     except:
#         rootCatId = None
#
#     try:
#         shopId = int(re.search(shopId_pattern, response.text).group(1))
#     except:
#         shopId = None
#
#     try:
#         shop_name = re.search(shop_name_pattern, response.text).group(1)
#         shop_name = parse.unquote(shop_name)
#     except:
#         shop_name = None
#
#     try:
#         brand_name = re.search(brand_name, response.text).group(1)
#     except:
#         brand_name = None
#
#     try:
#         brand_id = int(re.search(brand_id, response.text).group(1))
#     except:
#         brand_id = None
#     # try:
#     #     status = int(re.search(status_pattern, response.text).group(1))
#     # except:
#     #     status = -2
#     #
#     # if status == 0:
#     #     buy_enable = True
#     # else:
#     #     buy_enable = False
#
#     print(categoryId, rootCatId, shopId, shop_name, brand_name, brand_id)

