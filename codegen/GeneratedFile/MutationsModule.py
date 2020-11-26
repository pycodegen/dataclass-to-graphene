from typing import Optional

from codegen.GeneratedFile import GeneratedFile
from codegen.ModulePath import ModulePath


class GeneratedMutationsFile(GeneratedFile):
    def __init__(
            self,
            module_path: Optional[ModulePath] = None,
    ):
        super().__init__(
            module_path or ModulePath('graphql_generated.mutations')
        )
