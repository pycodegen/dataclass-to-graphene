from typing import Dict, TypeVar, Callable

TKey = TypeVar("TKey")
TValue = TypeVar("TValue")


def get_or_else_dict(
        dictionary: Dict[TKey, TValue],
        key: TKey,
        else_value: Callable[[], TValue],
) -> TValue:
    if key in dictionary:
        return dictionary[key]
    else:
        return else_value()
