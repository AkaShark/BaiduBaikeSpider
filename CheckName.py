from urllib.parse import urlencode
from BaiduCrawler import BaiduCrawler


class CheckName(object):
    def __init__(self, content):
        self.content = content

    def createUrl(self):
        url = urlencode(self.content)
        return url

    def request(self):
        crawler = BaiduCrawler(self.createUrl(), 'baidu')

