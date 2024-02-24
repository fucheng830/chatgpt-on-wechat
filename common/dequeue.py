from queue import Full, Queue
from time import monotonic as time
"""
此代码实现了一个名为 Dequeue 的类，它继承自 Python 标准库中的 Queue 类并添加了一个新的方法 putleft，从而为这个队列类提供了双端队列（deque）的功能。以下是对代码主要部分的功能逐一解释：
"""

# add implementation of putleft to Queue
class Dequeue(Queue):
    def putleft(self, item, block=True, timeout=None):
        with self.not_full:
            if self.maxsize > 0:
                if not block:
                    if self._qsize() >= self.maxsize:
                        raise Full
                elif timeout is None:
                    while self._qsize() >= self.maxsize:
                        self.not_full.wait()
                elif timeout < 0:
                    raise ValueError("'timeout' must be a non-negative number")
                else:
                    endtime = time() + timeout
                    while self._qsize() >= self.maxsize:
                        remaining = endtime - time()
                        if remaining <= 0.0:
                            raise Full
                        self.not_full.wait(remaining)
            self._putleft(item)
            self.unfinished_tasks += 1
            self.not_empty.notify()

    def putleft_nowait(self, item):
        return self.putleft(item, block=False)

    def _putleft(self, item):
        self.queue.appendleft(item)
