from typing import Set, Optional

from py_type_extractor.type_extractor.nodes.BaseNodeType import NodeType
from py_type_extractor.type_extractor.nodes.ClassFound import ClassFound

from codegen.BaseCodegen import BaseCodegen
from codegen.extractor_flags.is_query import is_query_flag
from codegen.idenfitier.__base__ import BaseIdentifier
from codegen.middleware_flags import BaseMiddlewareFlag
from codegen.middlewares.__base__ import BaseMiddleware


class QueryMiddleware(BaseMiddleware):
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


