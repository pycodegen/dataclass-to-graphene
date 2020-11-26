from typing import Optional

from py_type_extractor.type_extractor.nodes.BaseNodeType import NodeType

from codegen.BaseCodegen import BaseCodegen
from codegen.idenfitier.__base__ import BaseIdentifier
from codegen.middlewares.__base__ import BaseMiddleware


class BuiltinsMiddleware(BaseMiddleware):
    def process(
            self,
            node: NodeType,
            codegen: BaseCodegen,
    ) -> Optional[BaseIdentifier]:
        if node == int:
            pass

    ...