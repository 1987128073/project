import time


def timestamp_to_timestr(timeStamp):
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

def timestr_to_timestamp(timestr):
    # 字符类型的时间
    tss1 = '2013-10-10 23:40:00'
    # 转为时间数组
    timeArray = time.strptime(tss1, "%Y-%m-%d %H:%M:%S")
    # 转为时间戳
    timeStamp = int(time.mktime(timeArray))
    return timeStamp


if __name__ == '__main__':
    a = timestamp_to_timestr(1381419600)
    print(a)