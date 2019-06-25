from telgrab import TelGrab
from time import time


if __name__ == '__main__':
    start = time()
    for _ in TelGrab().parse_list(['https://hands.ru/company/about', 'https://repetitors.info/'] * 100, 10, 20):
        print(_)
    print('{0} seconds'.format(int(time() - start)))
