import trio
from typing import (
    List, TypeVar, Any, Awaitable, overload, Tuple, Coroutine,
)

_T1 = TypeVar('_T1')
_T2 = TypeVar('_T2')
_T3 = TypeVar('_T3')
_T4 = TypeVar('_T4')
_T5 = TypeVar('_T5')


@overload
def gather(
        coro_or_future1: Coroutine[Any, Any, _T1],
) -> Awaitable[Tuple[_T1]]: ...


@overload
def gather(
        coro_or_future1: Coroutine[Any, Any, _T1],
        coro_or_future2: Coroutine[Any, Any, _T2],
) -> Awaitable[Tuple[_T1, _T2]]: ...


@overload
def gather(
        coro_or_future1: Coroutine[Any, Any, _T1],
        coro_or_future2: Coroutine[Any, Any, _T2],
        coro_or_future3: Coroutine[Any, Any, _T3],
) -> Awaitable[Tuple[_T1, _T2, _T3]]: ...


@overload
def gather(
        coro_or_future1: Coroutine[Any, Any, _T1],
        coro_or_future2: Coroutine[Any, Any, _T2],
        coro_or_future3: Coroutine[Any, Any, _T3],
        coro_or_future4: Coroutine[Any, Any, _T4],
) -> Awaitable[Tuple[_T1, _T2, _T3, _T4]]: ...


@overload
def gather(
        coro_or_future1: Coroutine[Any, Any, _T1],
        coro_or_future2: Coroutine[Any, Any, _T2],
        coro_or_future3: Coroutine[Any, Any, _T3],
        coro_or_future4: Coroutine[Any, Any, _T4],
        coro_or_future5: Coroutine[Any, Any, _T5],
) -> Awaitable[Tuple[_T1, _T2, _T3, _T4, _T5]]: ...


async def gather(*tasks: List[Coroutine[Any, Any, Any]]):
    async def collect(index: int, task: Coroutine[Any, Any, Any], results):
        task_func, *task_args = task
        results[index] = await task_func(*task_args)

    results = {}
    async with trio.open_nursery() as nursery:
        for index, task in enumerate(tasks):
            nursery.start_soon(collect, index, task, results)
    return [results[i] for i in range(len(tasks))]


async def child(x: float) -> float:
    print(f"Child sleeping {x}")
    await trio.sleep(x)
    return 2 * x


async def parent():
    tasks = [(child, t) for t in range(2)]
    a = child(1)
    return await gather(
        child(1),
        child(2),
        trio.sleep(3),
    )


print("results:", trio.run(parent))
