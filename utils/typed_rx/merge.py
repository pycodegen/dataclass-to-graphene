from typing import TypeVar, cast, Union

import rx
# from rx.operators import * as ops
import rx.operators as ops

from typing_extensions import overload

T1 = TypeVar('T1')
T2 = TypeVar('T2')
T3 = TypeVar('T3')
T4 = TypeVar('T4')
T5 = TypeVar('T5')


@overload
def merge_(
        stream1: rx.typing.Subject[T1, T1],
        stream2: rx.typing.Subject[T2, T2],
) -> rx.typing.Observable[Union[T1, T2]]: pass # type: ignore

@overload
def merge_(
        stream1: rx.typing.Observable[T1],
        stream2: rx.typing.Observable[T2],
) -> rx.typing.Observable[Union[T1, T2]]: pass # type: ignore

def merge_(
        stream1: Union[
                rx.typing.Observable[T1],
                rx.typing.Subject[T1, T1],
        ],
        stream2: Union[
                rx.typing.Observable[T2],
                rx.typing.Subject[T2, T2],
        ],
) -> rx.typing.Observable[Union[T1, T2]]:
    return cast(rx.Observable, stream1)\
        .pipe(
            ops.merge(cast(rx.Observable, stream2))
        )
