import abc
from typing import Optional

from py_type_extractor.type_extractor.nodes.BaseNodeType import NodeType

from codegen.BaseCodegen import BaseCodegen
from codegen.idenfitier.__base__ import BaseIdentifier


class BaseMiddleware(
    metaclass=abc.ABCMeta,
):
    @abc.abstractmethod
    def process(
            self,
            node: NodeType,
            codegen: BaseCodegen,
    ) -> Optional[BaseIdentifier]:
        ...
