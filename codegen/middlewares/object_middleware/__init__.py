from typing import Optional, Set, NewType

from py_type_extractor.type_extractor.nodes.BaseNodeType import NodeType
from py_type_extractor.type_extractor.nodes.ClassFound import ClassFound
from py_type_extractor.type_extractor.nodes.TypeOR import TypeOR

from codegen.BaseCodegen import BaseCodegen
from codegen.GeneratedFile.generated_file_pool import GeneratedFilePool, get_generated_file, get_generated_module_path
from codegen.ModulePath.FromTypeExtractor.from_class_found import from_class_found
from codegen.ModulePath.RootModulePath import RootModulePath
from codegen.idenfitier.IdentifierWithImport import IdentifierWithImport
from codegen.idenfitier.ListIdentifier import ListIdentifier
from codegen.idenfitier.OptionalIdentifier import OptionalIdentifier
from codegen.idenfitier.__base__ import BaseIdentifier
from codegen.middlewares.__base__ import BaseMiddleware
from codegen.middlewares.object_middleware.from_original_type_codegen import FromOriginalTypeCodegen
from codegen.middlewares.object_middleware.graphene_fields_defs_codegen import GrapheneFieldsDefCodegen
from codegen.middlewares.object_middleware.process_imports import process_imports
from codegen.middlewares.object_middleware.process_resolver_funcs import process_resolver_funcs
from codegen.middlewares.object_middleware.to_original_type_codegen import ToOriginalType
from utils.optional_node_utils import is_optional_typeor, typeor_discard_optional


class ObjectMiddleware(BaseMiddleware):
    def __init__(
            self,
            generated_file_pool: GeneratedFilePool,
            root_module_path: RootModulePath,
    ):
        self.generated_file_pool = generated_file_pool
        self.root_module_path = root_module_path

    def process(
            self,
            node: NodeType,
            codegen: BaseCodegen,
    ) -> Optional[BaseIdentifier]:
        if not isinstance(node, ClassFound):
            return None

        src_module_path = from_class_found(node)
        generated_module_path = get_generated_module_path(
            root_module_path=self.root_module_path,
            src_module_path=src_module_path,
        )
        generated_file = get_generated_file(
            generated_file_pool=self.generated_file_pool,
            module_path=generated_module_path,
        )
        to_original_type_codegen = ToOriginalType()
        from_original_type_codegen = FromOriginalTypeCodegen()
        graphene_fields_def_codegen = GrapheneFieldsDefCodegen()

        for key,field_node in node.fields.items():
            identifier = codegen._process(field_node)
            process_imports(
                generated_file=generated_file,
                identifier=identifier,
            )
            to_original_type_codegen.add_field(
                name=key,
                identifier=identifier,
            )
            from_original_type_codegen.add_field(
                name=key,
                identifier=identifier,
            )
            graphene_fields_def_codegen.add_field(
                name=key,
                identifier=identifier,
            )

        # resolvers
        resolvers = process_resolver_funcs(node.methods)





    # ...
    # def process(self, node: NodeType) -> BaseIdentifier:
    #     if not isinstance(node, ClassFound):
