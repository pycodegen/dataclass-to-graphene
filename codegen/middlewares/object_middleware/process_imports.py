from codegen.GeneratedFile import GeneratedFile
from codegen.idenfitier.IdentifierWithImport import IdentifierWithImport
from codegen.idenfitier.ListIdentifier import ListIdentifier
from codegen.idenfitier.OptionalIdentifier import OptionalIdentifier
from codegen.idenfitier.__base__ import BaseIdentifier


def process_imports(
        generated_file: GeneratedFile,
        identifier: BaseIdentifier,
):
    if isinstance(identifier, OptionalIdentifier) \
            or isinstance(identifier, ListIdentifier):
        a = identifier.wrapped
        if isinstance(a, IdentifierWithImport):
            generated_file.add_import(a.module)
            return
    if isinstance(identifier, IdentifierWithImport):
        generated_file.add_import(identifier.module)

