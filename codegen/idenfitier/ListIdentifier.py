from typing import List, Union

from codegen.idenfitier.IdentifierWithImport import IdentifierWithImport
from codegen.idenfitier.OptionalIdentifier import OptionalIdentifier
from codegen.idenfitier.__base__ import BaseIdentifier, WrappedIdentifier


"""
아예:
 - List[Optional[A]] --> is_list_optional = [True]
 -   Optional[List[
"""


class ListIdentifier(WrappedIdentifier):
    """
    is_optional_list:
    Optional[List[A] --> is_optional_list = [T] / wrapped: A
    List[Optional[List[A]] --> is_optional_list = [F, T] / wrapped: A
    ---    ----------
    List[Optional[List[Optional[A]] --> is_optional_list = [F, T] / wrapped: Optional[A]
    ---   -----------
    """
    is_optional_list: List[bool]
    wrapped: Union[IdentifierWithImport, OptionalIdentifier]

    def __init__(
            self,
            is_optional_list: List[bool],
            wrapped: BaseIdentifier,
    ):
        self.is_optional_list = is_optional_list
        self.wrapped = wrapped