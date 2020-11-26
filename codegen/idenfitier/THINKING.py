# "identifier" --> (import_module + name) ?
from typing import Dict, Set


class ImportMap:
    module_path_identifier: Dict[str, Set[str]]

    def add(self, module_path: str, identifier_str: str):
        identifier_set = self.module_path_identifier.get(module_path) or set()
        identifier_set.add(identifier_str)
        self.module_path_identifier[module_path] = identifier_set
        return self  # for chaining
