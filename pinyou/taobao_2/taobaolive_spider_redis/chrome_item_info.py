import re
import time
from urllib import parse
from selenium import webdriver as wb
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from config import chrome_url_list

ops = Options()
ops.add_experimental_option('excludeSwitches', ['enable-automation'])
# ops.add_argument('--proxy-server=http://127.0.0.1:8080')

browser = wb.Chrome(executable_path='./WebDriver/chromedriver', chrome_options=ops, )
#
# browser = wb.Remote(
#             command_executor=chrome_url_list[2].get('url'),
#             desired_capabilities=DesiredCapabilities.CHROME,
#             # options=ops
#         )

def get_item_info(itemId):
    taobao_goods_url = 'https://item.taobao.com/item.htm?ft=t&id={}'
    base_url = taobao_goods_url.format(itemId)  # 600024278481
    browser.get(url=base_url)
    # time.sleep(2)
    if 'tmall.com' in browser.current_url:
        cid_pattern = re.compile(r',categoryId:(\d*?),', re.S)
        rcid_pattern = re.compile(r'name="rootCatId" value="(\d*?)"', re.S)
        shopId_pattern = re.compile(r"; shopId=(\d*?);", re.S)
        shop_name_pattern = re.compile(r'sellerNickName:"(.*?)",', re.S)
        brand_name = re.compile(r'"brand":"(.*?)",', re.S)
        brand_id = re.compile(r',"brandId":"(.*?)",', re.S)
        status_pattern = re.compile(r'"auctionStatus":"(.*?)",', re.S)

    else:
        cid_pattern = re.compile(r" cid\s*: '(\d*?)'", re.S)
        rcid_pattern = re.compile(r"rcid\s*: '(\d*?)'", re.S)
        shopId_pattern = re.compile(r" shopId\s*: '(\d*?)'", re.S)
        shop_name_pattern = re.compile(r" shopName\s*: '(.*?)'", re.S)
        status_pattern = re.compile(r" status\s*: (.*?),", re.S)
        brand_name = re.compile(r'"brand":"(.*?)",', re.S)
        brand_id = re.compile(r',"brandId":"(.*?)",', re.S)

    response = browser.page_source
    print(response)

    if '很抱歉，您查看的宝贝不存在' in response:
        categoryId = None
        rootCatId = None
        shopId = None
        shop_name = None
        buy_enable = False
        flag = 0
        close_brower()
        return categoryId, rootCatId, shopId, shop_name, buy_enable, flag

    # category_id
    try:
        categoryId = int(re.search(cid_pattern, response).group(1))
    except:
        categoryId = None

    # root_category_id
    try:
        rootCatId = int(re.search(rcid_pattern, response).group(1))
    except:
        rootCatId = None

    # shop_id
    try:
        shopId = int(re.search(shopId_pattern, response).group(1))
    except:
        shopId = None

    # shop_name
    try:
        shop_name = re.search(shop_name_pattern, response).group(1)
        shop_name = parse.unquote(shop_name)
    except:
        shop_name = None

    # brand_name
    try:
        brand_name = re.search(brand_name, response).group(1)
        brand_name = parse.unquote(brand_name).encode('utf-8').decode('utf-8')
    except:
        brand_name = None

    # brand_id
    try:
        brand_id = int(re.search(brand_id, response).group(1))
    except:
        brand_id = None

    # is_sell? 0->ture, -2->false
    try:
        status = int(re.search(status_pattern, response).group(1))
    except:
        status = -2

    if status == 0:
        buy_enable = True
    else:
        buy_enable = False
    flag = 0

    print('categoryId:{}, rootCatId:{}, shopId:{}, shop_name:{}, buy_enable:{},brand_id:{}, brand_name:{}'.format(
        categoryId, rootCatId, shopId, shop_name, buy_enable, brand_id, brand_name))

    close_brower()

    return categoryId, rootCatId, shopId, shop_name, buy_enable, flag


def close_brower():
    # browser.quit()
    pass


if __name__ == '__main__':
    get_item_info(602895195088)
    # item_list = [9618854849, 602894391801, 602895195088]
    # for i in item_list:
    #     get_item_info(i)