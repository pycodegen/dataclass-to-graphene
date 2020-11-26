import threading

from typing import Callable, Any


class ThreadedInterval(threading.Thread):
    def __init__(
            self,
            callback_fn: Callable[[int], Any],
            interval: float,
    ):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.count = 0
        self.callback_fn = callback_fn
        self.interval = interval

    def run(self):
        while not self.event.is_set():
            self.callback_fn(self.count)
            self.count += 1
            self.event.wait(self.interval)

    def stop(self):
        self.event.set()


if __name__ == '__main__':
    import time
    tmr = ThreadedInterval(lambda a: print(a), 0.5)
    tmr.start()
    time.sleep(3)
    tmr.stop()
