import abc

from codegen.ModulePath import ModulePath
from codegen.idenfitier.__base__ import BaseIdentifier


class IdentifierWithImport(BaseIdentifier, metaclass=abc.ABCMeta):
    module: ModulePath
    name: str

    def __init__(
            self,
            module: ModulePath,
            name: str,
    ):
        self.module = module
        self.name = name

