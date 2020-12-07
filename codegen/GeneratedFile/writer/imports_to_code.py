from codegen.GeneratedFile import GeneratedFile


def imports_to_code(generated_file: GeneratedFile):
    return '\n'.join([
        f'import {i}'
        for i in list(generated_file.imports)
    ])
