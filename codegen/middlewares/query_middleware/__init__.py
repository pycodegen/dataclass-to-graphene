import textwrap
from typing import Set, Optional, Dict

from py_type_extractor.type_extractor.nodes.BaseNodeType import NodeType
from py_type_extractor.type_extractor.nodes.ClassFound import ClassFound

from codegen.BaseCodegen import BaseCodegen
from codegen.GeneratedFile.generated_file_pool import get_generated_module_path, get_generated_file, GeneratedFilePool
from codegen.ModulePath.FromTypeExtractor.from_class_found import from_class_found
from codegen.ModulePath.RootModulePath import RootModulePath
from codegen.extractor_flags import is_query_flag
from codegen.idenfitier import PossibleIdentifiers
from codegen.idenfitier.GeneratedGrapheneObjectIdentifier import GeneratedGrapheneObjectIdentifier
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
from codegen.middlewares.query_middleware.process_resolver_funcs import get_raw_resolvers, ResolverFuncCodegen
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

        generated_file.add_import(src_module_path)

        to_original_type_codegen = ToOriginalObjCodegen(
            get_original_obj_ident(node)
        )
        from_original_type_codegen = FromOriginalObjCodegen()
        graphene_fields_def_codegen = GrapheneFieldsDefCodegen()
        input_flags = flags | {is_input}
        output_flags = flags | {is_output}
        for key, field_node in node.fields.items():
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

        resolver_func_codegen = ResolverFuncCodegen()
        resolvers_raw = get_raw_resolvers(node.methods)
        for name, raw_resolver in resolvers_raw.items():
            args_idents: Dict[str, PossibleIdentifiers] = {
                args_name: codegen._process(
                    node=args_node,
                    flags=input_flags,
                )
                for args_name, args_node in raw_resolver.params.items()
            }
            return_ident = codegen._process(
                node=raw_resolver.return_type,
                flags=output_flags,
            )
            resolver_func_codegen.add_resolver(
                name=name,
                args_idents=args_idents,
                return_ident=return_ident,
            )

        class_body = strip_margin(f"""
        |{graphene_fields_def_codegen.generate_code()}
        |
        |{to_original_type_codegen.print_code()}
        |
        |{from_original_type_codegen.print_code()}
        |
        |{resolver_func_codegen.print_code()}
        |
        |...
        """)
        generated_file.add_code(
            strip_margin(f"""
            |# from query_middleware
            |class {node.name}(graphene.ObjectType):
            |{textwrap.indent(class_body, '    ')}
            |
            """)
        )

        return GeneratedGrapheneObjectIdentifier(
            module=generated_module_path,
            name=node.name,
        )