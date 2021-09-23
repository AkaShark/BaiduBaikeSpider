import json

NaN = float('nan')
PosInf = float('inf')
NegInf = float('-inf')

_CONSTANTS = {
    '-Infinity': NegInf,
    'Infinity': PosInf,
    'NaN': NaN,
}

_KEYS = ['__dict__', '__doc__', '__module__', '__weakref__']


class JsonDecoder(object):
    def __init__(self, *, object_hook=None, parse_float=None,
                 parse_int=None, parse_constant=None, strict=True,
                 object_pairs_hook=None):
        self.object_hook = object_hook
        self.parse_float = parse_float or float
        self.parse_int = parse_int or int
        self.parse_constant = parse_constant or _CONSTANTS.__getitem__
        self.strict = strict
        self.object_pairs_hook = object_pairs_hook

    def decode(self, s, mClass):
        try:
            data = json.loads(s, object_hook=self.object_hook, parse_float=self.parse_float,
                              parse_int=self.parse_int, parse_constant=self.parse_constant, strict=self.strict,
                              object_pairs_hook=self.object_pairs_hook)
        except Exception as err:
            raise json.JSONDecodeError("Json Loads Error", s, err.__str__())
        return self.__transform__(data, mClass)

    def __transform__(self, data, mClass):
        if data.__class__ == list:
            result = [self.__dictToModel__(d, mClass) for d in data]
        elif data.__class__ == dict:
            result = self.__dictToModel__(data, mClass)
        return result

    def __dicToModel__(self, d, mClass):
        m = mClass()
        doc = getattr(mClass, "__doc__")
        for key in self.__keys__(mClass):
            if doc and key in doc.keys():
                setattr(m, key, self.__transform__(d.get(key), doc[key]))
            else:
                setattr(m, key, d.get(key))
        return m

    def __keys__(self, mClass):
        for key in dir(mClass):
            if not callable(getattr(mClass, key)) and key not in _KEYS:
                yield key
