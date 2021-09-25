"""
bs4 version 4.9.3
没有做代理池 如果需要可以在manager中添加设置
生成的Verified.csv 需要再次验证下
"""
# encoding='utf-8'
from BaiduCrawler import BaiduCrawler
from Config import Config
from Manager import Manager
from FileOperation import FileOperation
from Util import CrawlerType

if __name__ == '__main__':
    manager = Manager()
    header = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.8',
        'Cache-Control': 'max-age=0',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
        'Connection': 'keep-alive',
    }
    cookie = None
    config = Config(header, cookie)
    manager.set_config(config)
    filePath = './aircraftName.csv'
    contents = FileOperation(filePath).read()
    queryNames = []
    for content in contents:
        content = content.split(',')[1]
        content = content.strip('\n')
        queryNames.append(content)
    manager.set_queryNames(queryNames)

    # 百度百科爬虫
    baidu = BaiduCrawler(crawled=True, type=CrawlerType.Aircraft)
    baidu.run()
