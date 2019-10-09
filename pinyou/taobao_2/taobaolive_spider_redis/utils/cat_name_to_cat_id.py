import pymysql
from pymongo import MongoClient

from config import environments


def catName_to_catId(env):
    env_dict = environments.get(env)
    clent = MongoClient(env_dict.get('mongodb_host'), port=env_dict.get('mongodb_port'))
    mongo_db = clent['v3_app_data_parsed']

    db = pymysql.connect(host=env_dict.get('mysql_host'),  # 数据库服务器IP
                         port=env_dict.get('mysql_port'),
                         user=env_dict.get('mysql_user'),
                         passwd=env_dict.get('mysql_pwd'),
                         db=env_dict.get('db'))  # 数据库名称

    # 使用cursor()方法创建一个游标对象cur
    cur = db.cursor()
    mongo_cur = mongo_db['products'].find({})
    for i in mongo_cur:
        _id = i.get('_id')
        tao_leaf_categoryname = i.get('top_leaf_categoryname')
        tao_category_name = i.get('root_categoryname')
        # 使用execute()执行SQL语句
        cur.execute("select tao_leaf_category_id, taobao_category from pl_taobao_category where tao_leaf_category_name='{}' and taobao_category_name='{}';".format(tao_leaf_categoryname, tao_category_name))

        # 使用 fetchone() 方法获取一条数据
        data = cur.fetchone()

        if not data:
            continue
        else:
            top_leaf_categoryid = data[0]
            root_categoryid = data[1]
            mongo_db['products'].update_one({'_id': _id}, {"$set": {'top_leaf_categoryid': top_leaf_categoryid, 'root_categoryid': root_categoryid}})
     # 关闭数据库连接
    db.close()


def catId_to_catName(env):
    env_dict = environments.get(env)
    clent = MongoClient(env_dict.get('mongodb_host'), port=env_dict.get('mongodb_port'))
    mongo_db = clent['v3_app_data_parsed']

    db = pymysql.connect(host=env_dict.get('mysql_host'),  # 数据库服务器IP
                         port=env_dict.get('mysql_port'),
                         user=env_dict.get('mysql_user'),
                         passwd=env_dict.get('mysql_pwd'),
                         db=env_dict.get('db'))  # 数据库名称

    # 使用cursor()方法创建一个游标对象cur
    cur = db.cursor()
    mongo_cur = mongo_db['products'].find({})
    for i in mongo_cur:
        _id = i.get('_id')
        tao_leaf_categoryid = i.get('top_leaf_categoryid')
        tao_category = i.get('root_categoryid')
        # 使用execute()执行SQL语句
        cur.execute("select tao_leaf_category_name, taobao_category_name from pl_taobao_category where tao_leaf_category_id='{}' and taobao_category='{}';".format(tao_leaf_categoryid, tao_category))

        # 使用 fetchone() 方法获取一条数据
        data = cur.fetchone()

        if not data:
            continue
        else:
            top_leaf_category_name = data[0]
            root_category_name = data[1]
            mongo_db['products'].update_one({'_id': _id}, {"$set": {'top_leaf_categoryname': top_leaf_category_name, 'root_categoryname': root_category_name}})
     # 关闭数据库连接
    db.close()


if __name__ == '__main__':
    catName_to_catId('dev')