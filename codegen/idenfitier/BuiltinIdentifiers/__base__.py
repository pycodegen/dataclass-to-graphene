from abc import ABCMeta

from codegen.ModulePath import ModulePath
from codegen.idenfitier.IdentifierWithImport import IdentifierWithImport
from codegen.idenfitier.__base__ import BaseIdentifier


class BaseBuiltinIdentifier(IdentifierWithImport, metaclass=ABCMeta):
    def __init__(self):
        self.module = ModulePath('graphene')