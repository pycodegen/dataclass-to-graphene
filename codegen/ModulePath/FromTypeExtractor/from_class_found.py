from py_type_extractor.type_extractor.nodes.ClassFound import ClassFound

from codegen.ModulePath import ModulePath


def from_class_found(class_found: ClassFound):
    return ModulePath(class_found.module_name)