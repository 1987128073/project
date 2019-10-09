import configparser
import os


class ReadConfig:
    def __init__(self, filepath=None):

        if filepath:
            configpath = filepath
        else:
            root_dir = os.path.dirname(os.path.abspath('.'))
            configpath = os.path.join(root_dir, 'config.ini')
        self.cf = configparser.ConfigParser()
        self.cf.read(configpath)

    def get_db(self, param):
        try:
            value = self.cf.get(param[0], param[1])
        except:
            raise
        return value


if __name__ == '__main__':
    test = ReadConfig()
    t = test.get_db(['Mysql', 'host'])