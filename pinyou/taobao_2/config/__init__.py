from .dev import dev
from .pro import pro
from .test import test

environments = {
    'dev': dev,
    'pro': pro,
    'test': test
}

chrome_url_list = [
    {'url': 'http://192.168.1.45:30003/wd/hub', 'statue': 0},
    {'url': 'http://192.168.1.63:30004/wd/hub', 'statue': 0},
    {'url': 'http://192.168.1.45:30002/wd/hub', 'statue': 0},
    {'url': 'http://192.168.1.45:30001/wd/hub', 'statue': 0},
]