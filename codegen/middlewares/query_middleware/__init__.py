import textwrap
from typing import Set, Optional

from py_type_extractor.type_extractor.nodes.BaseNodeType import NodeType
from py_type_extractor.type_extractor.nodes.ClassFound import ClassFound

from codegen.BaseCodegen import BaseCodegen
from codegen.GeneratedFile.generated_file_pool import get_generated_module_path, get_generated_file, GeneratedFilePool
from codegen.ModulePath.FromTypeExtractor.from_class_found import from_class_found
from codegen.ModulePath.RootModulePath import RootModulePath
from codegen.extractor_flags.is_query import is_query_flag
from codegen.idenfitier.OriginalObjIdentifier import get_original_obj_ident
from codegen.idenfitier.__base__ import BaseIdentifier
from codegen.middleware_flags import BaseMiddlewareFlag, is_input, is_output
from codegen.middlewares.__base__ import BaseMiddleware
from codegen.middlewares.__codegens__.graphene_typ_def import (
    GrapheneFieldsDefCodegen,
)
from codegen.middlewares.__codegens__.type_conversion import (
    ToOriginalObjCodegen,
    FromOriginalObjCodegen,
)
from codegen.middlewares.__utils__.process_import import process_import
from utils.lang.strip_margin import strip_margin

"""
class SomeQuery:
    
"""

class QueryMiddleware(BaseMiddleware):
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
            flags: Set[BaseMiddlewareFlag],
    ) -> Optional[BaseIdentifier]:
        if not isinstance(node, ClassFound):
            return None
        if not node.options.__contains__(is_query_flag):
            return None
        # must be query!

        src_module_path = from_class_found(node)

        generated_module_path = get_generated_module_path(
            root_module_path=self.root_module_path,
            src_module_path=src_module_path,
        )

        generated_file = get_generated_file(
            generated_file_pool=self.generated_file_pool,
            module_path=generated_module_path,
        )

        to_original_type_codegen = ToOriginalObjCodegen(
            get_original_obj_ident(node)
        )
        from_original_type_codegen = FromOriginalObjCodegen()
        graphene_fields_def_codegen = GrapheneFieldsDefCodegen()
        input_flags = flags | { is_input }
        output_flags = flags | { is_output }
        for key,field_node in node.fields.items():
            field_identifier = codegen._process(
                field_node, flags=output_flags,
            )
            process_import(
                generated_file=generated_file,
                identifier=field_identifier,
            )
            to_original_type_codegen.add_field(
                name=key,
                identifier=field_identifier,
            )
            from_original_type_codegen.add_field(
                name=key,
                identifier=field_identifier,
            )
            graphene_fields_def_codegen.add_field(
                name=key,
                identifier=field_identifier,
            )



        generated_file.add_code(
            strip_margin(f"""
            |class {node.name}(graphene.Object):
            |{textwrap.indent(
                graphene_fields_def_codegen.generate_code(), 
                ' ' * 4
            )}
            |{textwrap.indent(
                to_original_type_codegen.print_code(),
                '    ')}
            |{textwrap.indent(
                from_original_type_codegen.print_code(), 
                '    ')}
            |    ... # in case the object is empty
            |"""))
