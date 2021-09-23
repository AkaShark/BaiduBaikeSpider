from enum import Enum, unique, auto

class KeyMapping(object):
    def __init__(self):
        self.attrMap = {
            "翼展": "wingspan",
            "长度": "length",
            "高度": "height",
            "主轮距": "mainWheelPitch",
            "前主轮距": "frontMainPitch",
            "正常起飞重量": "normalTakeoff",
            "最大起飞重量": "maximumTakeoffWeight",
            "外挂能力": "plugInCapacity",
            "机内燃油": "fuel",
            "最大马赫数": "maximumMachNumber",
            "实用升限": "practicalLimit",
            "起飞滑跑距离": "takeOffDistance",
            "着陆滑跑距离": "landingDistance",
            "航程": "range",
            "限制过载": "limitOverload",

        }
        self.relMap = {
            "中文名": "chineseName",
            "外文名": "englishName",
            "前型/级": "flowed",
            "研制时间": "developmentTime",
            "服役时间": "attendedTime",
            "研制国家": "developedCountries",
            "装备国家": "equipmentState",
            "飞机类型": "theAircraftType",
            "首飞时间": "theFirstFlightTime"
        }

    def attrMapping(self):
        return self.attrMap

    def relMapping(self):
        return self.relMap


@unique
class CrawlerType(Enum):
    Aircraft = auto()
    Ship = auto()


def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner
