from typing import TypeVar, Callable, cast, Union

import rx
from rx import operators as ops

from typing_extensions import overload

T1 = TypeVar('T1')
T2 = TypeVar('T2')
T3 = TypeVar('T3')
T4 = TypeVar('T4')
T5 = TypeVar('T5')


@overload
def filter_(
        stream: rx.typing.Subject[T1, T1],
        filter_func: Callable[[T1], bool],
) -> rx.typing.Observable[T1]: pass

@overload
def filter_(
        stream: rx.typing.Observable[T1],
        filter_func: Callable[[T1], bool],
) -> rx.typing.Observable[T1]: pass

def filter_(
        stream: Union[rx.typing.Observable[T1], rx.typing.Subject[T1, T1]],
        filter_func: Callable[[T1], bool]
) -> rx.typing.Observable[T1]:
    return cast(rx.Observable, stream).pipe(ops.filter(filter_func))