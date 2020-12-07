import pathlib
from os import sep

from codegen.GeneratedFile import GeneratedFile
from codegen.GeneratedFile.writer.imports_to_code import imports_to_code
from utils.lang.strip_margin import strip_margin


def write_generated_file(
        generated: GeneratedFile,
        root_folder: pathlib.Path,
):
    module_path = generated.module_path.replace('.', sep)
    module_folder = root_folder / module_path
    print('module_folder:', module_folder)
    module_folder.mkdir(parents=True, exist_ok=True)
    filename = module_folder.joinpath('__init__.py').absolute()
    code = strip_margin(
        f"""
        |{imports_to_code(generated)}
        |
        |{generated.code}
        |"""
    )
    with open(filename, 'w') as f:
        f.write(code)