import csv

import redis
import xlrd
def getcategroy_exl():
    # r=redis.StrictRedis(host='192.168.1.45', port=6379, db=0, password='admin')
    wbk = xlrd.open_workbook(r'C:\Users\Admin\PycharmProjects\pinyou\goodsdata\goodsdata\file\keywords.csv')
    mysheet =wbk.sheet_by_index(1)
    nrows = mysheet.nrows
    list = []
    for i in range(1, nrows):
        myrowvalues = mysheet.row_values(i)[0]
        list.append(myrowvalues)
    # for category in set(list):
    #     r.sadd('goods_category_set', category)
    return set(list)

def getcategroy_csv():
    list = []
    with open(r'C:\Users\Admin\PycharmProjects\pinyou\goodsdata\goodsdata\file\keywords.csv', 'r', encoding='utf-8',
              newline='') as f:
        csv_data = csv.reader(f, dialect='excel')
        for i in csv_data:
            # print(i)
            list.append(i[0])

if __name__ == '__main__':
    getcategroy_csv()

