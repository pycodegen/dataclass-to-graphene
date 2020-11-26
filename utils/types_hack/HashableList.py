import collections

from typing import List, Generic, TypeVar, Optional

TItem = TypeVar('TItem')


class HashableList(  # type: ignore
    List[TItem],
    collections.UserList,  # type: ignore
    Generic[TItem],
):
    def __hash__(self):
        return hash(tuple(self))

    def to_string(self):
        return '__'.join(self)