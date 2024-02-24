"""
这段代码定义了一个名为 `singleton` 的装饰器，用于实现单例模式。单例模式是一种设计模式，确保一个类只有一个实例，并提供一个全局访问点。

以下是 `singleton` 装饰器的功能：

1. 定义了一个名为 `instances` 的字典，用于存储类的实例。
2. 定义了一个名为 `get_instance` 的内部函数，用作实际的类构造器。
3. 当用 `singleton` 装饰器装饰一个类时，如果有尝试创建新对象的动作，`get_instance`函数会被调用。
4. `get_instance` 函数检查 `instances` 字典中是否已经存在对应类的实例。
5. 如果实例已存在，就直接返回该实例；如果不存在，就创建一个新实例，存入 `instances` 字典，然后返回新创建的实例。

通过这种方式，无论创建多少次对象，经过 `singleton` 装饰的类都只会有一个实例被创建。这在需要确保资源只被初始化一次或当实例的创建开销很大时非常有用。
"""

def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance
