from typing import List

from codegen.idenfitier.__base__ import BaseIdentifier, WrappedIdentifier


class ListIdentifier(WrappedIdentifier):
    """
    is_nullable_list:

    Optional[List[A] --> is_nullable_list = [True]

    List[Optional[List[A]] --> is_nullable_list = [False, True]
    """
    is_nullable_list: List[bool]
    wrapped: BaseIdentifier

    def __init__(
            self,
            is_nullable_list: List[bool],
            wrapped: BaseIdentifier,
    ):
        self.is_nullable_list = is_nullable_list
        self.wrapped = wrapped

    def to_string(self) -> str:
        pass