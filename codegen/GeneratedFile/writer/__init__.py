import pathlib

from codegen.GeneratedFile.generated_file_pool import GeneratedFilePool
from codegen.GeneratedFile.writer.imports_to_code import imports_to_code
from codegen.GeneratedFile.writer.write_generated_file import write_generated_file


def write_generated_file_pool(
        generated_file_pool: GeneratedFilePool,
        root_folder: pathlib.Path,
):
    for module_path, generated_file in generated_file_pool.items():
        write_generated_file(
            generated=generated_file,
            root_folder=root_folder,
        )
