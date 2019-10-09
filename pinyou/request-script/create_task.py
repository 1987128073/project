import redis
from pymongo import MongoClient


class TaskRedis(object):

    def __init__(self, db):
        self.r = redis.StrictRedis(host='192.168.1.45', password='admin', db=db)
        self.cli = MongoClient('192.168.1.45')
        self.db = self.cli['pltaobao']
        self.collection1 = self.db['checktask']
        self.collection2 = self.cli['Task']['CheckItemIdTask']

    def pushtask(self, task):
        if self.taskname == 'itemid':
            if not self.checkliveidtask(task):
                self.r.sadd('itemid', task)
                self.collection2.insert_one({'_id': str(task)})
        elif self.taskname == 'liveid':
            if not self.checktask(task):
                self.r.sadd('liveid', task)
                self.collection1.insert_one({'_id': str(task)})

    def checktask(self, task):
        res = self.collection1.find_one({'_id': str(task)})
        if res:
            return 1
        else:
            return 0

    def checkliveidtask(self, task):
        res = self.collection2.find_one({'_id': str(task)})
        if res:
            return 1
        else:
            return 0

    def run(self, task, taskname):
        self.taskname = taskname
        self.pushtask(task)

    def get_task(self,taskname):
        self.taskname = taskname
        if taskname == 'liveid':
            for a in self.db['LiveId'].find({}).skip(110000).limit(10000):
                self.pushtask(a.get('_id'))
        elif taskname == 'itemid':
            for a in self.db['itemId'].find({}):
                self.pushtask(a.get('_id'))

    def push_itemId(self, taskname):
        self.taskname = taskname
        num = 0
        while 1:
            count = 10000
            cur = self.db['tb_anchor_goods'].find({}).skip(count * num).limit(10000)
            print(count * num)
            if not cur:
                break
            num += 1
            for a in cur:
                self.pushtask(a.get('itemId'))

    def push_(self, taskname):
        self.r.sadd('anchorId_task', taskname)


if __name__ == '__main__':
    task = TaskRedis(db=1)
    # task.run()
    # task.push_itemId('itemid')
    # task.get_task('liveid')

    task.push_(taskname='1862807471')