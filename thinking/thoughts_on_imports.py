"""
note that we only need the following imports everywhere:
"""
from dataclasses import dataclass


@dataclass
class ImportModuleAliasMap:
    module_path: str
    alias: str

@dataclass
class ImportsMap:
    root_module_path: str  #

    @property
    def src_import(self):
        return ImportModuleAliasMap(module_path=)