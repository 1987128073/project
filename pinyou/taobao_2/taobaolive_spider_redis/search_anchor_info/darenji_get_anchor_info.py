import redis
import requests
from pymongo import MongoClient
from requests_html import HTMLSession
from config import environments


class AnchorInfo(object):

    def __init__(self, env):
        self.url = 'http://www.darenji.com/search.html'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36',
            'Referer': 'http://www.darenji.com/search.html',
        }
        self.env_dict = environments.get(env)
        self.r = redis.StrictRedis().from_url(url=self.env_dict.get('redis_url'))
        self.clent = MongoClient(self.env_dict.get('mongodb_host'), port=self.env_dict.get('mongodb_port'))
        self.db = self.clent['pltaobao']
        self.session = HTMLSession()

    def save_data(self, id, nickname, fansCount, anchorPhoto, houseId, descText):
        self.r.sadd('anchorId', str(id))
        self.r.sadd('anchorName', nickname)
        collection = self.db['anchor_info']
        res = collection.find_one({'anchorId': str(id)})
        if not res:
            data = {

                'anchorId': str(id),
                'anchorName': nickname,
                'houseId': int(houseId),
                'fansCount': int(fansCount),
                'liveCount': None,
                'city': None,
                'creatorType': None,
                'darenScore': None,
                'descText': descText,
                'anchorPhoto': anchorPhoto,
                'organId': None,
                'fansFeature': None,
                'historyData': None,
            }
            collection.insert_one(data)

    def get_data(self, anchor_name):

        try:
            rs = self.session.post(url=self.url, headers=self.headers, data={'conditions': anchor_name}, timeout=3)
        except:
            return None

        find_count = rs.html.xpath('//*[@id="qcount"]/text()')[0]

        if find_count == '0':
            return None

        nick_list = rs.html.xpath('//*[@id="nickname"]/text()')
        anchorPhoto_list = rs.html.xpath('//*[@id="paginate"]/li/div/a/@style')
        fans_num = rs.html.xpath('//*[@id="paginate"]/li/div/div[1]/h1/span/text()')
        house_id = rs.html.xpath('//*[@id="paginate"]/li/div/div[1]/p/span/text()')
        desc_text = rs.html.xpath('//*[@id="paginate"]/li/div/div[2]/div[1]/p/text()')

        for index, nick in enumerate(nick_list):
            id = anchorPhoto_list[index].split('/')[5]
            nickname = nick_list[index].replace(' ', '').replace("\n", "")
            fansCount = fans_num[index].replace(' 粉丝数量：', '')
            anchorPhoto = anchorPhoto_list[index].replace('background:url(', 'https:').replace(') no-repeat;', '')
            houseId = house_id[index]
            descText = desc_text[index].strip().replace("\n", "")
            print(id, nickname)
            if nickname == anchor_name:
                anchorId = id
                self.save_data(id, nickname, fansCount, anchorPhoto, houseId, descText)
                break
            else:
                anchorId = None
                # self.save_data(id, nickname, fansCount, anchorPhoto, houseId, descText)

        print(anchorId)
        return anchorId


if __name__ == '__main__':
    ai = AnchorInfo('dev')
    ai.get_data('世纪工匠')