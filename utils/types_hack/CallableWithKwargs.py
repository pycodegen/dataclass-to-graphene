from typing import TypeVar, Union, Callable, Any
from typing_extensions import Protocol

T_contra = TypeVar('T_contra', contravariant=True)
T_co = TypeVar('T_co', covariant=True)


class CallbackWithKwargs1(Protocol[T_contra, T_co]):
    def __call__(self,
                 __element: T_contra,  # type: ignore
                 __arg1=...,  # type: ignore
                 ) -> T_co:  # type: ignore
        pass


class CallbackWithKwargs2(Protocol[T_contra, T_co]):
    def __call__(self,
                 __element: T_contra,  # type: ignore
                 __arg1=...,  # type: ignore
                 __arg2=...,  # type: ignore
                 ) -> T_co:  # type: ignore
        pass


class CallbackWithKwargs3(Protocol[T_contra, T_co]):
    def __call__(self,
                 __element: T_contra,  # type: ignore
                 __arg1=...,  # type: ignore
                 __arg2=...,  # type: ignore
                 __arg3=...,  # type: ignore
                 ) -> T_co:
        pass


class CallbackWithKwargs4(Protocol[T_contra, T_co]):
    def __call__(self,
                 __element: T_contra,  # type: ignore
                 __arg1=...,  # type: ignore
                 __arg2=...,  # type: ignore
                 __arg3=...,  # type: ignore
                 __arg4=...,  # type: ignore
                 ) -> T_co:
        pass


class CallbackWithKwargs5(Protocol[T_contra, T_co]):
    def __call__(self,
                 __element: T_contra,  # type: ignore
                 __arg1=...,  # type: ignore
                 __arg2=...,  # type: ignore
                 __arg3=...,  # type: ignore
                 __arg4=...,  # type: ignore
                 __arg5=...,  # type: ignore
                 ) -> T_co:
        pass


CallbackWithKwargs = Union[
    CallbackWithKwargs1,
    CallbackWithKwargs2,
    CallbackWithKwargs3,
    CallbackWithKwargs4,
    CallbackWithKwargs5,
]
AnyCallable = Union[
    Callable[[Any], Any],
    Callable[[Any, Any], Any],
    Callable[[Any, Any, Any], Any],
    Callable[[Any, Any, Any, Any], Any],
    Callable[[Any, Any, Any, Any, Any], Any],
    Callable[[Any, Any, Any, Any, Any, Any], Any],
    Callable[..., Any],
]