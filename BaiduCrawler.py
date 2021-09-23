import json
import urllib
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from Crawler import Crawler
from Json2Model import Json2ModelAPI
from Manager import Manager
import requests
import pandas as pd
from Util import CrawlerType, KeyMapping
import pandas as pd
import numpy as np
from Model import Aircraft
import jsonModel

modelList = []
attrMapping = KeyMapping().attrMapping()
relMapping = KeyMapping().relMapping()


class BaiduCrawler(Crawler):
    def __init__(self, crawled=False, type=CrawlerType.Aircraft):
        self.manager = Manager()
        self.verifiedUrls = []
        self.verifiedNames = []
        self.crawled = crawled
        self.type = type
        if self.type == CrawlerType.Aircraft:
            self.filePath = "verifiedAircraft.csv"
        else:
            self.filePath = "./verifiedShip.csv"

    def run(self):
        if not self.crawled:
            self.checkVerify()
            self.writeFile()
        else:
            self.crawlerAllNameByVerifiedFile(self.filePath)

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
                content = self.sampleRequest(url, '#body_wrapper > div.searchResult > dl > dd:nth-child(2) > a')
                nextUrl = content[0]['href']  # 只取第一个
                nextName = content[0].next
                if nextUrl is not None and nextName is not None:
                    self.verifiedUrls.append(nextUrl)
                    self.verifiedNames.append(nextName)
                else:
                    self.verifiedUrls.append('')
                    self.verifiedNames.append('')

    def sampleRequest(self, url, patten):
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
        # 读取url构造爬虫
        urlsDataFrame = pd.read_csv(filePath, usecols=[3])
        nurls = np.array(urlsDataFrame)
        urls = nurls.reshape(1, len(nurls)).tolist()[0]
        for url in urls:
            aircraft = Aircraft()
            if str(url).startswith('/'):
                url = "https://baike.baidu.com" + url
            # 重构请求类
            request = requests.get(url, headers=self.manager.get_config().headers)
            soup = BeautifulSoup(request.text, 'lxml')

            # 解析对应的字段
            name = soup.select(
                "body > div.body-wrapper > div.content-wrapper > div > div.main-content.J-content > dl.lemmaWgt-lemmaTitle.lemmaWgt-lemmaTitle- > dd > h1")
            if name is not None and len(name) > 0:
                aircraft.name = name[0].text
            img = soup.select(
                "body > div.body-wrapper > div.content-wrapper > div > div.side-content > div.summary-pic > a > img")
            if img is not None and len(img) > 0:
                aircraft.img = img[0]['src']
            contentString = ""
            for para in soup.findAll(attrs={'class': 'para'}):
                contentString += para.text
            aircraft.content = contentString
            # 解析 表格数据
            self.analysisTableData("basic-info J-basic-info cmn-clearfix", soup, aircraft, False)
            # self.analysisTableData('', soup, aircraft, True)
            modelList.append(aircraft)

        self.modelToJson()

    def analysisTableData(self, patten, soup, model, isAttr=False):
        itemDivText = soup.find(attrs={"class": patten})
        if itemDivText is not None:
            itemDivText = itemDivText.text
        itemArray = []
        if itemDivText is not None:
            itemArray = itemDivText.split('\n\n')
        if itemArray is None or len(itemArray) == 0:
            return
        tableDataArray = []
        for item in itemArray:
            if len(item) <= 0:
                continue
            item = item.strip('\n')
            tableDataArray.append(item)

        keys = []
        values = []
        for index in range(0, len(tableDataArray), 2):
            item = tableDataArray[index]
            item = item.replace('\xa0', '')
            keys.append(item)
        for index in range(1, len(tableDataArray), 2):
            item = tableDataArray[index]
            item = item.replace('\xa0', '')
            values.append(item)
        dataDic = dict(zip(keys, values))

        # mapping
        for key, value in dataDic.items():
            if isAttr:
                if key in attrMapping:
                    model.attribute.__setattr__(attrMapping[key], value)
            else:
                if key in relMapping:
                    model.relation.__setattr__(relMapping[key], value)



    def modelToJson(self):
       jsonStr = json.dumps(obj=modelList,
                  default=lambda x: x.__dict__, sort_keys=False, indent=2)
       f = open('./dataModel.json', 'w', encoding='utf-8')
       f.write(jsonStr)
       f.close()

