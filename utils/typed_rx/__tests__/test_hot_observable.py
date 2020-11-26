import time

import rx
from typing import Optional

from utils.test_utils.threaded_interval import ThreadedInterval
from utils.typed_rx.to_hot_observable import to_hot_observable


def interval_stream_subscriber(
        observer: rx.typing.Observer[str],
        scheduler: Optional[rx.typing.Scheduler],
):
    def next_func(i: int):
        observer.on_next(i)
        print(f'got i: {i}')
    print('inside interval_stream_subscriber')
    interval = ThreadedInterval(
        callback_fn=next_func,
        interval=0.5
    )
    interval.start()

    return IntervalStreamDisposable(interval)


class IntervalStreamDisposable(rx.typing.Disposable):
    def __init__(self, interval: ThreadedInterval):
        self.interval = interval

    def dispose(self) -> None:
        self.interval.stop()


interval_stream: rx.typing.Observable[int] = rx.create(interval_stream_subscriber)
# #
hot_interval_stream = to_hot_observable(
    base_stream=interval_stream,
)

class CustomObserver(rx.typing.Observer[int]):
    def __init__(self, observer_name: str):
        self.observer_name = observer_name
    def on_next(self, value: int) -> None:
        print(f"CustomObserver {self.observer_name} got: {value}")

    def on_error(self, error: Exception) -> None:
        pass

    def on_completed(self) -> None:
        pass

# subscription1 = result.subscribe(CustomObserver('observer1'))

subscription1 = hot_interval_stream.subscribe(CustomObserver('observer1'))

subscription2 = hot_interval_stream.subscribe(CustomObserver('observer2'))


print('aa')
time.sleep(3)

subscription1.dispose()
print('bb')

time.sleep(2)

subscription2.dispose()

time.sleep(3)
subscription3 = hot_interval_stream.subscribe(CustomObserver('observer3'))
time.sleep(2)
subscription3.dispose()
