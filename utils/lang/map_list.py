from typing import TypeVar, List, Callable, Optional

TTo = TypeVar('TTo')
TFrom = TypeVar('TFrom')


# Q.

def map_list(
        func: Callable[[TFrom], TTo],
) -> Callable[[Optional[List[TFrom]]], Optional[List[TTo]]]:
    def list_func(l: Optional[List[TFrom]]) -> Optional[List[TTo]]:
        if l is None:
            return None
        return [func(item) for item in l]

    return list_func


if __name__ == '__main__':
    def int_to_str(a: int) -> str:
        return str(a)


    result = map_list(
        map_list(
            int_to_str,
        )
    )([[1, 2, 3], [1, 3, 5]])

    print(result)
    #
    # reveal_type(result)
