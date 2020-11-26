import rx
from typing import TypeVar, Tuple, cast, Optional, Any

from typing_extensions import overload


T1 = TypeVar('T1')
T2 = TypeVar('T2')
T3 = TypeVar('T3')
T4 = TypeVar('T4')
T5 = TypeVar('T5')

@overload
def combine_latest(
        s1: rx.typing.Observable[T1],
) -> rx.typing.Observable[Tuple[T1]]: ...

@overload
def combine_latest(
        s1: rx.typing.Observable[T1],
        s2: rx.typing.Observable[T2],
) -> rx.typing.Observable[Tuple[T1,T2]]: ...

@overload
def combine_latest(
        s1: rx.typing.Observable[T1],
        s2: rx.typing.Observable[T2],
        s3: rx.typing.Observable[T3],
) -> rx.typing.Observable[Tuple[T1,T2,T3]]: ...

def combine_latest(
        # *streams: rx.typing.Observable,
        s1: Optional[rx.typing.Observable[T1]] = None,
        s2: Optional[rx.typing.Observable[T2]] = None,
        s3: Optional[rx.typing.Observable[T3]] = None,
) -> Any:
    return rx.combine_latest(cast(rx.Observable, [s1, s2, s3]))
