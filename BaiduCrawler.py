import urllib
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from Crawler import Crawler
from Manager import Manager
import requests
import pandas as pd
from Util import CrawlerType

filePath = "./verified.csv"

class BaiduCrawler(Crawler):
    def __init__(self, crawled=False, type=CrawlerType.Aircraft):
        self.manager = Manager()
        self.verifiedUrls = []
        self.verifiedNames = []
        self.crawled = crawled
        self.type = type
        if self.type == CrawlerType.Aircraft:
            self.filePath = "./verifiedAircraft.csv"
        else:
            self.filePath = "./verifiedShip.csv"

    def run(self):
        if not self.crawled:
            self.checkVerify()
            self.writeFile()
        else:
            self.crawlerAllNameByVerifiedFile(filePath)

    def checkVerify(self):
        for name in self.manager.get_queryNames():
            url = 'https://baike.baidu.com/item/' + urllib.parse.quote(name)
            title = self.request(url,
                                 'body > div.body-wrapper > div.content-wrapper > div > div.main-content.J-content > dl.lemmaWgt-lemmaTitle.lemmaWgt-lemmaTitle- > dd > h1')
            if title is not None and len(title) > 0:
                self.verifiedUrls.append(url)
                self.verifiedNames.append(name)
            else:
                url = 'https://baike.baidu.com/search/none?word=' + urllib.parse.quote(name)
                content = self.request(url, '#body_wrapper > div.searchResult > dl > dd:nth-child(2) > a')
                nextUrl = content[0]['href']
                nextName = content[0].next.next
                if nextUrl is not None and nextName is not None:
                    self.verifiedUrls.append(nextUrl)
                    self.verifiedNames.append(nextName)
                else:
                    self.verifiedUrls.append('')
                    self.verifiedNames.append('')

    def request(self, url, patten):
        request = requests.get(url, headers=self.manager.get_config().headers)
        soup = BeautifulSoup(request.text, 'lxml')
        content = soup.select(patten)
        return content

    def writeFile(self):
        if self.checkArray():
            # 字典中的key值即为csv中列名
            dataframe = pd.DataFrame(
                {'origin_name': self.manager.get_queryNames(), 'verify_name': self.verifiedNames,
                 'url': self.verifiedUrls})
            # 将DataFrame存储为csv,index表示是否显示行名，default=True
            dataframe.to_csv(self.filePath, index=False, sep=',')

    def checkArray(self):
        if len(self.verifiedUrls) == len(self.manager.get_queryNames()):
            return True
        return False

    def crawlerAllNameByVerifiedFile(self, filePath):
        pass
