import csv
import os

import redis
import requests
from lxml import etree
class GetPic(object):
    headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'cookie': 'enc=QrRQ6DeUOmYLzYIkQbfBcg97wu8djvmnrbgkmfQX%2BGGAa4xXv1F%2Fotzxof%2FON15NcqzbCC8ho7txae3Jj9znYw%3D%3D;',
            'referer': 'https://v.taobao.com/v/content/live?spm=a21xh.11312869.fastEntry.8.75a8627fl7u5OW&catetype=702',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }
    def __init__(self):
        self.id = None
        self.name = None
        self.number = 0

    def save_pic(self, url, num):
        url = 'http:' + url

        isExists = os.path.exists('./goods2/{}'.format(self.name))
        if isExists:
            r = requests.get(url=url, headers=self.headers)
            with open('./goods2/{}/{}.jpg'.format(self.name, num), 'ab') as f:
                f.write(r.content)
        else:
            os.makedirs('./goods2/{}'.format(self.name))
            r = requests.get(url=url, headers=self.headers)
            with open('./goods2/{}/{}.jpg'.format(self.name, num), 'ab') as f:
                f.write(r.content)

    def save_l_pic(self,url,word):
        print(url)
        url = 'http:'+ url
        r = requests.get(url=url, headers=self.headers)
        with open('./goods2/{}/{}.jpg'.format(self.name, word), 'ab') as f:
            f.write(r.content)

    def run(self):
        # r = redis.StrictRedis(host='192.168.1.45', port=6379, db=0, password='admin')
        # while 1:
        #     url = r.spop('goodsurl')
        #     if not url:
        #         break
        #     self.get_picture_url(url.decode('utf-8'))
        with open(r'C:\Users\Admin\PycharmProjects\pinyou\Anchor\csv\goods2.csv', 'r') as f:
            csv_data = csv.reader(f, dialect='excel')
            for a in csv_data:
                try:
                    id = a[1].split('=')[-1]
                    self.name = a[0]+'_' + id
                    self.get_picture_url(a[1])
                    # print(self.number)
                    self.number += 1
                except Exception as e:
                    continue

    def get_picture_url(self, url):
        self.id = url.split('=')[-1]
        response = requests.get(url=url, headers=self.headers)
        html = etree.HTML(response.text)
        lis = html.xpath('//*[@id="J_UlThumb"]/li//img/@data-src')
        print(len(lis), self.id)

        littles = html.xpath('//*[@id="J_isku"]/div/dl[2]/dd/ul/li/a/@style')
        if not littles:
            littles = html.xpath('//*[@id="J_isku"]/div/dl[2]/dd/ul/li/a/@style')

        words = html.xpath('//*[@id="J_isku"]/div/dl[2]/dd/ul/li/a/span/text()')
        if not words:
            words = html.xpath('//*[@id="J_isku"]/div/dl[1]/dd/ul/li/a/span/text()')
        print(littles, words)
        num = 1
        for li in lis:
            pic_url = li[:-10]
            # print(pic_url, self.id)
            self.save_pic(pic_url, num)
            num += 1
        if not words:

            for little, word in zip(littles, words):
                l_pic_url = little[15:-29]
                print(l_pic_url, word)
                try:
                    word = word.replace('/', '')
                except:
                    word = word
                # print(l_pic_url, word)
                self.save_l_pic(l_pic_url, word)


if __name__ == '__main__':
    getpic = GetPic()
    getpic.run()