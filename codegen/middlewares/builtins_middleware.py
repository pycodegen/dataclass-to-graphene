from typing import Optional, Set

from py_type_extractor.type_extractor.nodes.BaseNodeType import NodeType

from codegen.BaseCodegen import BaseCodegen
from codegen.idenfitier.BuiltinIdentifiers import (
    int_identifier,
    float_identifier, str_indentifier,
)
from codegen.idenfitier.__base__ import BaseIdentifier
from codegen.middleware_flags.__base__ import BaseMiddlewareFlag
from codegen.middlewares.__base__ import BaseMiddleware


class BuiltinsMiddleware(BaseMiddleware):
    def process(
            self,
            node: NodeType,
            codegen: BaseCodegen,
            flags: Set[BaseMiddlewareFlag],
    ) -> Optional[BaseIdentifier]:
        if node == int:
            return int_identifier
        if node == float:
            return float_identifier
        if node == str:
            return str_indentifier

        return None

    ...