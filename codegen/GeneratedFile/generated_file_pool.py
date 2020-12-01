from typing import Dict

from codegen.GeneratedFile import GeneratedFile
from codegen.GeneratedFile.__base__ import GeneratedModulePath
from codegen.ModulePath import ModulePath
from codegen.ModulePath.RootModulePath import RootModulePath

GeneratedFilePool = Dict[GeneratedModulePath, GeneratedFile]


def get_generated_module_path(
        root_module_path: RootModulePath,
        src_module_path: ModulePath,
) :
    return GeneratedModulePath(
        ModulePath(f'{root_module_path}.{src_module_path}')
    )


def get_generated_file(
        generated_file_pool: GeneratedFilePool,
        module_path: GeneratedModulePath,
) -> GeneratedFile:
    generated_file = generated_file_pool.get(module_path)
    if generated_file is None:
        new_file = GeneratedFile(
            module_path=module_path,
        )
        generated_file_pool[module_path] = new_file
        return new_file
    return generated_file
