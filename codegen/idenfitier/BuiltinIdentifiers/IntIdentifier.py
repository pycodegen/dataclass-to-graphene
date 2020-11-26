from dataclasses import dataclass

from codegen.ModulePath import ModulePath
from codegen.idenfitier.BuiltinIdentifiers import BaseBuiltinIdentifier

@dataclass
class IntIdenfier(BaseBuiltinIdentifier):
    def to_string(self) -> str:
        return f'{self.module}.Int'