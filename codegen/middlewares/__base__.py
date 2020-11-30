import abc
from typing import Optional, Set

from py_type_extractor.type_extractor.nodes.BaseNodeType import NodeType

from codegen.BaseCodegen import BaseCodegen
from codegen.idenfitier.__base__ import BaseIdentifier
from codegen.middleware_flags.__base__ import BaseMiddlewareFlag


class BaseMiddleware(
    metaclass=abc.ABCMeta,
):
    @abc.abstractmethod
    def process(
            self,
            node: NodeType,
            codegen: BaseCodegen,
            flags: Set[BaseMiddlewareFlag],
    ) -> Optional[BaseIdentifier]:
        ...
