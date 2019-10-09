import getopt
import sys


def a(argv):
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["env=", "device_id="])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt == 'env':
            print('xxx.py -env dev -device_id 123456')
            sys.eixt()
        elif opt in ('-env'):
            env = arg
        elif opt in ('-device_id'):
            device_id = arg

    print(env)
    print(device_id)


if __name__ == '__main__':
    a(sys.argv[1:])