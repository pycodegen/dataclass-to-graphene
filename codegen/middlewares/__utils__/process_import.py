from codegen.GeneratedFile import GeneratedFile
from codegen.idenfitier.IdentifierWithImport import IdentifierWithImport
from codegen.idenfitier.__base__ import BaseIdentifier, WrappedIdentifier


def process_import(
        generated_file: GeneratedFile,
        identifier: BaseIdentifier,
):
    if isinstance(identifier, WrappedIdentifier):
        a = identifier.wrapped
        if isinstance(a, IdentifierWithImport):
            generated_file.add_import(a.module)
            return
    if isinstance(identifier, IdentifierWithImport):
        generated_file.add_import(identifier.module)

