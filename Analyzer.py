"""
解析需要的数据 虚基类 具体需要的话需要继承实现自己的子类
"""


class Analyzer(object):
    def __int__(self, patten):
        self.patten = patten
