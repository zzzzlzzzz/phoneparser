import re
from multiprocessing import Pool

from requests import get
from requests.exceptions import RequestException
from bs4 import BeautifulSoup


class TelGrab:
    def __init__(self, timeout: 'float' = 10, user_agent: 'str' = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) '
                                                                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                                                                  'Chrome/50.0.2661.94 Safari/537.36'):
        self.timeout = timeout
        self.user_agent = user_agent

    def parse(self, url: 'str') -> 'tuple':
        try:
            page = get(url, headers={'User-Agent': self.user_agent}, timeout=self.timeout)
            page.raise_for_status()
        except RequestException:
            return url, []

        try:
            soup = BeautifulSoup(page.text, 'lxml')
        except:
            try:
                soup = BeautifulSoup(page.text, 'html5lib')
            except:
                return url, []

        for skip in soup(['script', 'style']):
            skip.extract()

        pattern = re.compile(r'(^|\D)(8[ (]{1,3}(\d{3})[ )]{1,3})?(\d{1,3})[ \-]{1,3}(\d{2})[ \-]{1,3}(\d{2})($|\D)')
        numbers = []
        for text in soup.find_all(text=True):
            for phone in pattern.findall(text):
                if phone[2]:
                    numbers.append(''.join(['8', phone[2], *phone[3:6]]))
                else:
                    numbers.append(''.join(['8495', *phone[3:6]]))

        return url, numbers

    def parse_list(self, urls: 'list', chunksize: 'int' = 1, cores: 'int' = None) -> 'tuple':
        with Pool(cores) as pool:
            for item in pool.imap_unordered(self.parse, urls, chunksize):
                yield item
