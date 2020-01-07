import csv
import json
import os
import time

import redis
from pymongo import MongoClient
from requests_html import HTMLSession
from utils.hh1024_get_anchorInfo import AnchorInfo as AI_hh1024
from utils.zhiboshuju_get_anchor_info import AnchorInfo as AI_zhiboshuju
from flask import Flask,render_template,request,redirect,url_for
from werkzeug.utils import secure_filename

r = redis.StrictRedis().from_url(url="")

r_2 = redis.StrictRedis(host='192.168.1.180', port=30378)  # 任务redis

app = Flask(__name__, template_folder="templates")


def check_anchor(anchorName):
    clent = MongoClient(host='192.168.1.180', port=32766)
    db = clent['v3_app_data_parsed']
    res = db['anchors'].find_one({'nick': anchorName})
    if res:
        return res.get('_id')
    else:
        return 0


def search(name):
    rs = r_2.get(f'anchor_name:{name}')

    if rs:
        flag = rs.decode('utf-8')
        if flag:
            return 1
        else:
            return 0

    anchor_id = check_anchor(name)
    if anchor_id:  # 若有该用户则直接push任务
        v = {
            'type': 'operate_broadcaster',
            'id': anchor_id
        }

        r_2.lpush('operate_broadcaster:tasks', json.dumps(v))
        r_2.set(f'anchor_name:{name}', 1, 1800)
        return 1
    else:
        res = {}
        anchor_info = AI_hh1024('pro')
        id = anchor_info.get_anchor_info(name)
        if id:
            res['anchorId'] = id
        else:
            anchor_info = AI_zhiboshuju('pro')
            res['anchorId'] = anchor_info.get_data(name)

        if res.get('anchorId'):
            anchorId = res.get('anchorId')

            v = {
                'type': 'operate_broadcaster',
                'id': anchorId
            }

            r_2.lpush('operate_broadcaster:tasks', json.dumps(v))
            r_2.set(f'anchor_name:{name}', 1, 1800)
            return 1
        else:
            r.sadd('anchorName:RoomId:uid', f'{name}:123:123')
            time.sleep(12)
            anchor_id = check_anchor(name)
            if anchor_id:
                return 1
            else:
                return 0


@app.route('/')
def index():
    return '''
    单个添加监控名单API: /anchor_name/(name) (eg:/anchor_name/李佳琦Au...)<br>
    以csv文件形式添加监控名单API:  /uploads  <br>
    '''


@app.route('/anchor_name/<name>')
def add_task(name):
    msg = search(name)
    if msg:
        return f'已找到该主播:{name},任务推送成功！'
    else:
        return f'未找到该主播:{name},请检查名字是否正确！'


@app.route('/uploads', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath, './static/uploads', secure_filename(f.filename))  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        l = []
        if f.filename.endswith('csv'):

            with open(upload_path, 'r',
                      encoding='utf-8') as f:
                csv_data = csv.reader(f, dialect='excel')

                for a in csv_data:
                    item = {}
                    msg = search(a[0])
                    item['name'] = a[0]
                    item['result'] = f'已找到该主播:{a[0]},任务推送成功！' if msg else f'未找到该主播:{a[0]},请检查名字是否正确！'
                    l.append(item)
            return render_template('result.html', l=l)

        if f.filename.endswith('xlsx'):
            pass

        return redirect(url_for('upload'))
    return render_template('xlsx.html')


@app.route('/word')
def word():
    session = HTMLSession()
    lu = session.get(url='https://tool.lu/timestamp/?page=1', headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'})
    word = {}
    try:
        word['word'] = lu.html.find('.note-container')[0].text
    except:
        word['word'] = 'error'
    return render_template('word.html', word=word)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
