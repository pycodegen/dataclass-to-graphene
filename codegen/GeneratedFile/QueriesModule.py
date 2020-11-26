from typing import Optional

from codegen.GeneratedFile import GeneratedFile
from codegen.GeneratedFile.generated_file_pool import get_generated_module_path
from codegen.ModulePath import ModulePath
from codegen.ModulePath.RootModulePath import RootModulePath


class GeneratedQueriesFile(GeneratedFile):
    def __init__(
            self,
            root_module_path: RootModulePath,
            module_path: Optional[ModulePath] = None,
    ):
        generated_module_path = get_generated_module_path(
            root_module_path,
            module_path or 'queries'
        )
        super().__init__(generated_module_path)
