from typing import Union

from codegen.idenfitier.IdentifierWithImport import IdentifierWithImport
from codegen.idenfitier.__base__ import BaseIdentifier, WrappedIdentifier


class OptionalIdentifier(WrappedIdentifier):
    # wrapped: can't be 'List':
    #   Optional[List[A]]
    #    --> ListIdentifier(
    #           is_optional_list = [False],
    #           wrapped = A
    #        )
    wrapped: Union[IdentifierWithImport]

    def __init__(
            self,
            wrapped: Union[IdentifierWithImport]
    ):
        self.wrapped = wrapped
