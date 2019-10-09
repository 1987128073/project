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


def zeroPoint():
    zeropoint = int(time.time()) - int(time.time() - time.timezone) % 86400
    return zeropoint


def get_today_zero_timestamp(now_time):
    # 今天0点的时间字符串
    timeStamp = float(now_time)
    timeArray = time.localtime(timeStamp)
    zeroTime = time.strftime("%Y-%m-%d 00:00:00", timeArray)
    # 时间字符串再转为时间戳
    timeArray_ex = time.strptime(zeroTime, "%Y-%m-%d %H:%M:%S")
    return int(time.mktime(timeArray_ex))


if __name__ == '__main__':
    a = get_today_zero_timestamp(1566701943)
    b = timestamp_to_timestr(1566701943)
    print(a,b)