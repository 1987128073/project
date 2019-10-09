import threading
from mongodb_teest import select_mongo,select_mongo_test

threads = []
t2 = threading.Thread(target=select_mongo)
threads.append(t2)
# t3 = threading.Thread(target=select_mongo_test)
# threads.append(t3)


if __name__ == '__main__':
    for t in threads:
        t.start()
