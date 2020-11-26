import rx
import rx.operators as ops
from typing import TypeVar, cast

T1 = TypeVar('T1')
T2 = TypeVar('T2')
T3 = TypeVar('T3')
T4 = TypeVar('T4')
T5 = TypeVar('T5')


def to_hot_observable(
        # subject_factory: Callable[[Optional[rx.typing.Scheduler]], rx.typing.Subject[T2, T3]],
        base_stream: rx.typing.Observable[T1],
) -> rx.typing.Observable[T1]:

    return cast(rx.Observable, base_stream)\
        .pipe(
        ops.publish(),
        ops.ref_count(),
    )