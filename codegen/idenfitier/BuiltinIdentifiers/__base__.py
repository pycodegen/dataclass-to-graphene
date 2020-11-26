from abc import ABCMeta

from codegen.ModulePath import ModulePath
from codegen.idenfitier.IdentifierWithImport import IdentifierWithImport
from codegen.idenfitier.__base__ import BaseIdentifier


class BaseBuiltinIdentifier(IdentifierWithImport):
    def __init__(
            self,
            name: str,
    ):
        self.module = ModulePath('graphene')
        self.name = name

    def to_string(self) -> str:
        return f'{self.module}.{self.name}'
