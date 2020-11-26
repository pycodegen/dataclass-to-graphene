import abc
from typing import (
    TypeVar,
    Generic, Union, Coroutine, Any,
)

TArgs = TypeVar('TArgs')
TResult = TypeVar('TResult')


class ResolverFn(
    Generic[TArgs, TResult],
    metaclass=abc.ABCMeta
):
    @abc.abstractmethod
    def resolve(
            self, args: TArgs,
    ) -> TResult:
        ...


class AsyncResolverFn(
    Generic[TArgs, TResult],
    metaclass=abc.ABCMeta
):
    @abc.abstractmethod
    def resolve(
            self, args: TArgs,
    ) -> Coroutine[Any, Any, TResult]:
        ...


Resolver = Union[
    ResolverFn[TArgs, TResult],
    AsyncResolverFn[TArgs, TResult]
]

