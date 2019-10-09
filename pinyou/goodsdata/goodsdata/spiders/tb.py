import time, json

import scrapy
from scrapy.extensions.closespider import CloseSpider
from scrapy.http import FormRequest
from scrapy.utils.project import get_project_settings

from ..utils.get_goods_category import getcategroy_csv
from ..utils.get_category import get_category
from ..utils.taobaodeveloper import makesign
from ..items import couponItem


class TbkItemCouponGet(scrapy.Spider):
    name = 'tb'

    def start_requests(self):
        list = getcategroy_csv()
        # q = get_category()
        # if q is None:
        #     raise CloseSpider('抓取完毕')
        settings = get_project_settings()
        cats = ['16']
        for a in list:
            for page_no in range(1, 6):
                time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                params = {
                    'method': 'taobao.tbk.dg.item.coupon.get',
                    'app_key': str(settings.get('APPKEY')),
                    'platform': '2',
                    'sign_method': 'md5',
                    'timestamp': time_str,
                    'v': '2.0',
                    'format': 'json',
                    'cat': str(cats[0]),
                    'adzone_id': str(settings.get('ADZONE')),
                    'page_no': str(page_no),
                    'page_size': '20',
                    'q': a
                }
                sign = makesign(settings.get('SECRET'), params)
                params['sign'] = sign
                yield FormRequest(
                    url=settings.get('GOODSURLAPI'),
                    method='POST',
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                      'Chrome/75.0.3770.100 Safari/537.36',
                        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    },
                    formdata=params,
                    meta={
                        'page': page_no,
                    }
                )

    def parse(self, response):
        # print(response.text)
        meta = response.meta
        # print('正在解析的页码{}'.format(meta['page']))
        coupons = json.loads(response.text).get('tbk_dg_item_coupon_get_response').get('results').get('tbk_coupon')
        for coupon in coupons:
            coupon_item = couponItem()
            coupon_item['category'] = coupon.get('category')
            coupon_item['commission_rate'] = coupon.get('commission_rate')
            coupon_item['coupon_click_url'] = coupon.get('coupon_click_url')
            coupon_item['coupon_end_time'] = coupon.get('coupon_end_time')
            coupon_item['coupon_info'] = coupon.get('coupon_info')
            coupon_item['coupon_remain_count'] = coupon.get('coupon_remain_count')
            coupon_item['coupon_start_time'] = coupon.get('coupon_start_time')
            coupon_item['coupon_total_count'] = coupon.get('coupon_total_count')
            coupon_item['item_description'] = coupon.get('item_description')
            coupon_item['item_url'] = coupon.get('item_url')
            coupon_item['nick'] = coupon.get('nick')
            coupon_item['num_iid'] = coupon.get('num_iid')
            coupon_item['pict_url'] = coupon.get('pict_url')
            coupon_item['seller_id'] = coupon.get('seller_id')
            coupon_item['shop_title'] = coupon.get('shop_title')
            coupon_item['title'] = coupon.get('title')
            coupon_item['user_type'] = coupon.get('user_type')
            coupon_item['volume'] = coupon.get('volume')
            coupon_item['zk_final_price'] = coupon.get('zk_final_price')
            yield coupon_item