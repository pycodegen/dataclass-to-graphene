from typing import Optional, List, Tuple, Set

from py_type_extractor.type_extractor.nodes.BaseNodeType import NodeType
from py_type_extractor.type_extractor.nodes.ListFound import ListFound
from py_type_extractor.type_extractor.nodes.TypeOR import TypeOR

from codegen.BaseCodegen import BaseCodegen
from codegen.idenfitier.ListIdentifier import ListIdentifier
from codegen.idenfitier.__base__ import BaseIdentifier
from codegen.middleware_flags import BaseMiddlewareFlag
from codegen.middlewares.__base__ import BaseMiddleware
from utils.optional_node_utils import is_optional_typeor, typeor_discard_optional


class ListMiddleware(BaseMiddleware):
    def process(
            self,
            node: NodeType,
            codegen: BaseCodegen,
            flags: Set[BaseMiddlewareFlag],
    ) -> Optional[BaseIdentifier]:
        if not isinstance(node, ListFound) and not (
                isinstance(node, TypeOR)
                and is_optional_typeor(node)
        ):
            return None

        is_nullable_list, identifier = process_list_node(
            is_nullable_list=[],
            node=node,
            codegen=codegen,
            flags=flags,
        )
        return ListIdentifier(
            is_nullable_list=is_nullable_list,
            wrapped=identifier,
        )


def process_list_node(
        is_nullable_list: List[bool],
        node: NodeType,
        codegen: BaseCodegen,
        flags: Set[BaseMiddlewareFlag],
) -> Tuple[List[bool], BaseIdentifier]:
    if isinstance(node, ListFound):
        is_nullable_list.append(False)
        return process_list_node(
            is_nullable_list=is_nullable_list,
            node=node.typ,
            codegen=codegen,
        )
    if isinstance(node, TypeOR) and is_optional_typeor(node):
        node_without_optional = typeor_discard_optional(node)
        if isinstance(node_without_optional, ListFound):
            is_nullable_list.append(True)
            return process_list_node(
                is_nullable_list=is_nullable_list,
                node=node_without_optional.typ,
                codegen=codegen,
            )
    # not: List or Optional[List]
    identifier = codegen._process(node, flags=flags)
    return (is_nullable_list, identifier)
