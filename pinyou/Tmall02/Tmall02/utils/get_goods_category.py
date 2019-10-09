import redis
import xlrd
def getcategroy():
    r=redis.StrictRedis(host='192.168.1.45', port=6379, db=0, password='admin')
    wbk = xlrd.open_workbook('../file/20keywords.xlsx')
    mysheet =wbk.sheet_by_index(1)
    nrows = mysheet.nrows
    list = []
    for i in range(1, nrows):
        myrowvalues = mysheet.row_values(i)[0]
        list.append(myrowvalues)
    # for category in set(list):
    #     r.sadd('goods_category_set', category)
    return  set(list)

if __name__ == '__main__':
    getcategroy()

