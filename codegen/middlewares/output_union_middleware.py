# import graphene
#
# class Human(graphene.ObjectType):
#     name = graphene.String()
#     born_in = graphene.String()
#
# class Droid(graphene.ObjectType):
#     name = graphene.String()
#     primary_function = graphene.String()
#
# class Starship(graphene.ObjectType):
#     name = graphene.String()
#     length = graphene.Int()
#
# class SearchResult(graphene.Union):
#     class Meta:
#         types = (Human, Droid, Starship)
import textwrap
from typing import Optional, Set

from py_type_extractor.type_extractor.nodes.BaseNodeType import NodeType
from py_type_extractor.type_extractor.nodes.TypeOR import TypeOR

from codegen.BaseCodegen import BaseCodegen
from codegen.GeneratedFile.generated_file_pool import GeneratedFilePool, get_generated_module_path, get_generated_file
from codegen.ModulePath import ModulePath
from codegen.ModulePath.RootModulePath import RootModulePath
from codegen.idenfitier import PossibleIdentifiers
from codegen.idenfitier.GeneratedGrapheneObjectIdentifier import GeneratedGrapheneObjectIdentifier
from codegen.middleware_flags import BaseMiddlewareFlag, is_output, is_input
from codegen.middlewares.__base__ import BaseMiddleware
from codegen.middlewares.__codegens__.graphene_typ_def.identifier_to_graphene_typ import (
    identifier_to_graphene_typ,
)
from codegen.middlewares.__utils__.ident_to_valid_python_name import ident_to_valid_python_name
from codegen.middlewares.__utils__.process_import import process_import
from utils.lang.strip_margin import strip_margin
from utils.optional_node_utils import is_optional_typeor


class OutputUnionMiddleware(BaseMiddleware):
    def __init__(
            self,
            generated_file_pool: GeneratedFilePool,
            root_module_path: RootModulePath,
    ):
        self.generated_file_pool = generated_file_pool
        self.root_module_math = root_module_path
        self.to_write_module = get_generated_module_path(
            root_module_path=root_module_path,
            src_module_path=ModulePath('__unions__')
        )
        self.to_write_file = get_generated_file(
            generated_file_pool=generated_file_pool,
            module_path=self.to_write_module,
        )
        self.to_write_file.add_import(ModulePath('graphene'))

    def process(
            self,
            node: NodeType,
            codegen: BaseCodegen,
            flags: Set[BaseMiddlewareFlag],
    ) -> Optional[PossibleIdentifiers]:
        if not isinstance(node, TypeOR) \
                or not flags.__contains__(is_output) \
                or flags.__contains__(is_input):
            return None
        if is_optional_typeor(node):
            raise RuntimeError('got Optional[A] in output_union_middleware', node)

        idents = [
            codegen._process(i, flags=flags)
            for i in node.nodes
        ]
        for n in idents:
            process_import(
                generated_file=self.to_write_file,
                identifier=n,
            )

        # heck ugly but really un-likely to overlap?
        union_name = '__UNION_WITH__'.join([
            ident_to_valid_python_name(ident)
            for ident in idents
        ])

        idents_meta_types_code = '\n'.join([f'{identifier_to_graphene_typ(a)},' for a in idents])

        code_to_write = strip_margin(f"""
        |class {union_name}(graphene.Union):
        |    class Meta:
        |        types = (
        |{textwrap.indent(idents_meta_types_code, ' ' * 12)}
        |        )
        |
        |""")
        self.to_write_file.add_code(code_to_write)

        return GeneratedGrapheneObjectIdentifier(
            module=self.to_write_module,
            name=union_name,
        )
