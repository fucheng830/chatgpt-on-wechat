import heapq

"""
这段代码实现了一个名为 `SortedDict` 的类，该类继承自标准Python字典（`dict`），并添加了一些特殊的行为来维护键值对的有序状态。`SortedDict` 允许用户指定一个排序函数和排序顺序来确定键值对的排序规则。以下是其功能和行为：

1. `__init__` 初始化函数：接受一个排序函数 `sort_func`，一个初始字典 `init_dict`，和一个用于确定排序方向的 `reverse` 布尔标志。初始化时，会使用 `sort_func` 对初始字典的条目进行排序，并将其放入堆 `self.heap` 中。

2. `__setitem__` 方法：当设置新的键值对时，将对键使用 `sort_func` 函数计算其优先级，并将键和这个计算出的优先级加入到堆中。如果键已经存在，会更新其在堆中的位置。

3. `__delitem__` 方法：删除键时，同时也会删除堆中与这个键对应的条目。

4. `keys` 方法：返回一个经过排序的键的列表。排序根据堆 `self.heap` 和排序方向 `self.reverse` 来确定。

5. `items` 方法：与 `keys` 方法类似，但返回的是排序后的 `(键, 值)` 对的列表。

6. `_update_heap` 方法：一个内部方法，用于更新堆的数据，当一个键的值发生变化时，这个方法将重新计算该键的优先级并更新堆。

7. `__iter__` 方法：定义了类的迭代器，使 `SortedDict` 可以直接通过迭代来获取排序后的键。

8. `__repr__` 方法：定义了类的字符串表现形式，以便在打印或查看 `SortedDict` 实例时提供有用的信息。

整体来看，`SortedDict` 是对Python标准字典的扩展，为字典提供了按照特定规则排序的功能。

"""
class SortedDict(dict):
    def __init__(self, sort_func=lambda k, v: k, init_dict=None, reverse=False):
        if init_dict is None:
            init_dict = []
        if isinstance(init_dict, dict):
            init_dict = init_dict.items()
        self.sort_func = sort_func
        self.sorted_keys = None
        self.reverse = reverse
        self.heap = []
        for k, v in init_dict:
            self[k] = v

    def __setitem__(self, key, value):
        if key in self:
            super().__setitem__(key, value)
            for i, (priority, k) in enumerate(self.heap):
                if k == key:
                    self.heap[i] = (self.sort_func(key, value), key)
                    heapq.heapify(self.heap)
                    break
            self.sorted_keys = None
        else:
            super().__setitem__(key, value)
            heapq.heappush(self.heap, (self.sort_func(key, value), key))
            self.sorted_keys = None

    def __delitem__(self, key):
        super().__delitem__(key)
        for i, (priority, k) in enumerate(self.heap):
            if k == key:
                del self.heap[i]
                heapq.heapify(self.heap)
                break
        self.sorted_keys = None

    def keys(self):
        if self.sorted_keys is None:
            self.sorted_keys = [k for _, k in sorted(self.heap, reverse=self.reverse)]
        return self.sorted_keys

    def items(self):
        if self.sorted_keys is None:
            self.sorted_keys = [k for _, k in sorted(self.heap, reverse=self.reverse)]
        sorted_items = [(k, self[k]) for k in self.sorted_keys]
        return sorted_items

    def _update_heap(self, key):
        for i, (priority, k) in enumerate(self.heap):
            if k == key:
                new_priority = self.sort_func(key, self[key])
                if new_priority != priority:
                    self.heap[i] = (new_priority, key)
                    heapq.heapify(self.heap)
                    self.sorted_keys = None
                break

    def __iter__(self):
        return iter(self.keys())

    def __repr__(self):
        return f"{type(self).__name__}({dict(self)}, sort_func={self.sort_func.__name__}, reverse={self.reverse})"
