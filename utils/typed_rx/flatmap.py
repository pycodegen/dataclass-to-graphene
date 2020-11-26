from typing import TypeVar, Callable, cast, Awaitable

import rx
from rx import operators as ops

from typing_extensions import overload

T1 = TypeVar('T1')
T2 = TypeVar('T2')
T3 = TypeVar('T3')
T4 = TypeVar('T4')
T5 = TypeVar('T5')


def flatmap(
        stream: rx.typing.Observable[T1],
        map_func: Callable[[T1], Awaitable[T2]]
) -> rx.typing.Observable[T2]:
    return cast(rx.Observable, stream).pipe(ops.map(map_func))