from datetime import datetime, timedelta
"""
这段代码定义了一个名为 `ExpiredDict` 的类，它继承自 Python 的内置字典（`dict`），并增加了元素过期的特性。每个字典项都有一个过期时间，当试图获取某个项时，如果当前时间超过了该项的过期时间，该项就会从字典中被自动删除，并抛出一个 `KeyError` 异常。`ExpiredDict` 类的行为和标准字典类似，但增加了以下功能:

1. `__init__` 方法：初始化 `ExpiredDict` 对象，并设置元素过期的时间（以秒为单位）。

2. `__getitem__` 方法：重写这个方法以实现在每次访问字典项时检查其是否过期。如果未过期，则更新该项的过期时间并返回值；如果已过期，则删除该项并抛出一个 `KeyError`。

3. `__setitem__` 方法：重写这个方法以在增加新的字典项时同时设置其过期时间。过期时间是通过当前时间加上初始化时设置的过期秒数来计算的。

4. `get` 方法：这是一个辅助方法，它尝试返回字典中对应的值，如果没有找到或者键已经过期，则返回一个默认值。

5. `__contains__` 方法：重写此方法以检查字典中是否存在某个键而不考虑其值。如果键存在并且值未过期，返回 `True`；否则返回 `False`。

6. `keys` 方法：返回一个键列表，列表中的键都是当前未过期的。

7. `items` 方法：返回一个包含所有未过期键值对的列表。

8. `__iter__` 方法：返回一个迭代器，可用于迭代所有未过期的键。

这个类可以用于需要自动清理老旧数据的场合，比如缓存系统，在该系统中数据在一定时间后变得无效，需要从缓存中移除。
"""

class ExpiredDict(dict):
    def __init__(self, expires_in_seconds):
        super().__init__()
        self.expires_in_seconds = expires_in_seconds

    def __getitem__(self, key):
        value, expiry_time = super().__getitem__(key)
        if datetime.now() > expiry_time:
            del self[key]
            raise KeyError("expired {}".format(key))
        self.__setitem__(key, value)
        return value

    def __setitem__(self, key, value):
        expiry_time = datetime.now() + timedelta(seconds=self.expires_in_seconds)
        super().__setitem__(key, (value, expiry_time))

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key):
        try:
            self[key]
            return True
        except KeyError:
            return False

    def keys(self):
        keys = list(super().keys())
        return [key for key in keys if key in self]

    def items(self):
        return [(key, self[key]) for key in self.keys()]

    def __iter__(self):
        return self.keys().__iter__()
