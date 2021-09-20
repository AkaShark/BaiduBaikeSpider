from enum import Enum, unique, auto


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
