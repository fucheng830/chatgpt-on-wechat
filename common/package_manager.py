import time

import pip
from pip._internal import main as pipmain

from common.log import _reset_logger, logger

"""
该Python代码块的作用如下：

1. 定义了一个名为 `install` 的函数，接受一个参数 `package`，调用 pip 的内部方法 `pipmain` 来安装指定的包。

2. 定义了一个名为 `install_requirements` 的函数，接受一个参数 `file`，调用 `pipmain` 来根据传入的要求文件安装相关的包，同时将安装后的包进行升级。升级完成后，会调用 `_reset_logger` 函数重置日志记录器。

3. 定义了一个名为 `check_dulwich` 的函数，该函数不接收参数。目的是检查模块 `dulwich` 是否已经安装，并在未安装的情况下尝试安装它。函数内部进行了两次尝试，如果首次尝试失败，则会等待3秒后再试一次。如果两次尝试后仍未能正确安装 `dulwich`，则会抛出 `ImportError` 异常。

注意：此代码直接使用 `pip._internal`，这不是推荐做法，因为 `pip` 的内部API可能会变化而导致依赖它的代码失效。官方推荐通过命令行接口来调用 `pip`。此外，直接通过脚本安装依赖操作应谨慎进行，因为它可能会导致环境问题。
"""

def install(package):
    pipmain(["install", package])


def install_requirements(file):
    pipmain(["install", "-r", file, "--upgrade"])
    _reset_logger(logger)


def check_dulwich():
    needwait = False
    for i in range(2):
        if needwait:
            time.sleep(3)
            needwait = False
        try:
            import dulwich

            return
        except ImportError:
            try:
                install("dulwich")
            except:
                needwait = True
    try:
        import dulwich
    except ImportError:
        raise ImportError("Unable to import dulwich")
