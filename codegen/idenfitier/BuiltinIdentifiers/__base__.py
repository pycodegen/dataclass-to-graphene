from abc import ABCMeta

from codegen.ModulePath import ModulePath
from codegen.idenfitier.IdentifierWithImport import IdentifierWithImport
from codegen.idenfitier.__base__ import BaseIdentifier


class BaseBuiltinIdentifier(IdentifierWithImport):
    def __init__(self, name: str):
        module = ModulePath('graphene')
        super().__init__(module, name)
        self.module = module
        self.name = name

