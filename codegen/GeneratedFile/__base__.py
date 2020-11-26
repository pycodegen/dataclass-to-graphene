from typing import Set, NewType

from codegen.ModulePath import ModulePath


GeneratedModulePath = NewType(
    'GeneratedModulePath',
    ModulePath,
)


class GeneratedFile:
    imports: Set[ModulePath]
    module_path: ModulePath

    code: str

    def __init__(
            self,
            module_path: ModulePath,
            imports: Set[ModulePath] = None,
            code: str = None
    ):
        self.module_path = module_path
        self.imports = imports or set()
        self.code = code or ''

    def add_import(self, module_path: ModulePath):
        self.imports.add(module_path)

    def add_code(self, code: str):
        self.code += '\n' + code
