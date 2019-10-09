import schedule


def a():
    print('111')


schedule.every(30).seconds.do(a)

while True:
    schedule.run_pending()