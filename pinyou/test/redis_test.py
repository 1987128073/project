import csv

import redis

r = redis.StrictRedis(host='192.168.1.45', port=6379, db=1, password='admin')
for i in r.smembers('anchorId_hot'):
    with open('anchorId.csv', 'r', encoding='utf-8') as f:
        csv_data = csv.reader(f, dialect='excel')
        for x in csv_data:
            if str(i.decode('utf-8')) == str(x[0]):
                continue
            r.sadd('anchorId', i.decode('utf-8'))