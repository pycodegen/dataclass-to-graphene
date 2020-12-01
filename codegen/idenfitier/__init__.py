from typing import Union

from codegen.idenfitier.IdentifierWithImport import IdentifierWithImport
from codegen.idenfitier.ListIdentifier import ListIdentifier
from codegen.idenfitier.OptionalIdentifier import OptionalIdentifier

PossibleIdentifiers = Union[
    OptionalIdentifier,
    ListIdentifier,
    IdentifierWithImport,
]