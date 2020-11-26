from typing import List, Tuple, TypeVar, cast, Dict

TKey = TypeVar('TKey')
TValue = TypeVar('TValue')


# PyCharm temporary hack...
def get_dict_items(a: Dict[TKey, TValue]) -> List[Tuple[TKey, TValue]]:
    return cast(List[Tuple[TKey, TValue]], a.items())