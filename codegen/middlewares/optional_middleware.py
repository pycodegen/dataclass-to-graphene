from typing import Optional

from py_type_extractor.type_extractor.nodes.BaseNodeType import NodeType
from py_type_extractor.type_extractor.nodes.TypeOR import TypeOR

from codegen.BaseCodegen import BaseCodegen
from codegen.idenfitier.OptionalIdentifier import OptionalIdentifier
from codegen.idenfitier.__base__ import BaseIdentifier
from codegen.middlewares.__base__ import BaseMiddleware
from utils.optional_node_utils import is_optional_typeor, typeor_discard_optional


class OptionalMiddleware(BaseMiddleware):
    def process(
            self,
            node: NodeType,
            codegen: BaseCodegen,
    ) -> Optional[BaseIdentifier]:
        if isinstance(node, TypeOR) and is_optional_typeor(node):
            node_without_typeor = typeor_discard_optional(node)
            identifier = codegen._process(node_without_typeor)
            return OptionalIdentifier(
                wrapped=identifier,
            )
        return None