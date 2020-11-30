from py_type_extractor.type_extractor.nodes.ClassFound import ClassFound

from codegen.ModulePath import ModulePath
from codegen.idenfitier.IdentifierWithImport import IdentifierWithImport


class OriginalObjIdentifier(IdentifierWithImport):
    pass


def get_original_obj_ident(node: ClassFound):
    return OriginalObjIdentifier(
        module=ModulePath(node.module_name),
        name=node.name,
    )