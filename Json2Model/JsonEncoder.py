import json

_KEYS = ['__dict__', '__doc__', '__module__', '__weakref__']
_CLASS = [int, float, bool, complex, str, dict]


def __keys__(model_class):
    for key in dir(model_class):
        if not callable(getattr(model_class, key)) and key not in _KEYS:
            yield key  # 生成key


class JsonEncoder(object):
    def __init__(self, skip_keys=False, ensure_ascii=True,
                 check_circular=True, allow_nan=True, sort_keys=False,
                 indent=None, separators=None, default=None):
        self.skip_keys = skip_keys
        self.ensure_ascii = ensure_ascii
        self.check_circular = check_circular
        self.allow_nan = allow_nan
        self.sort_keys = sort_keys
        self.indent = indent
        self.item_separator = separators
        self.default = default

    def encode(self, obj):
        r = self.__transform__(obj)
        return json.dumps(r, skipkeys=self.skip_keys, ensure_ascii=self.ensure_ascii,
                          check_circular=self.check_circular, allow_nan=self.allow_nan, sort_keys=self.sort_keys,
                          indent=self.indent, separators=self.item_separator, default=self.default)

    def __transform__(self, obj):
        if list == obj.__class__:
            result = [self.__modelToDict__(o) for o in obj]
        elif obj.__class__ not in _CLASS:
            result = self.__modelToDict__(obj)
        else:
            result = self.__modelToDict__(obj)
        return result

    def __modelToDict__(self, obj):
        if obj.__class__ in _CLASS:
            return obj
        result = dict()
        for key in __keys__(obj.__class__):
            value = getattr(obj, key)
            if value.__class__ not in _CLASS:
                result[key] = self.__transform__(value)
            else:
                result[key] = value
        return result
