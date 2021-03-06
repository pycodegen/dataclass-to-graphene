import abc
from typing import Set

from py_type_extractor.type_extractor.nodes.BaseNodeType import NodeType

from codegen.idenfitier import PossibleIdentifiers
from codegen.middleware_flags.__base__ import BaseMiddlewareFlag


class BaseCodegen(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add_query(self, query_class): ...

    @abc.abstractmethod
    def add_mutation(self, mutation_func): ...

    @abc.abstractmethod
    def add_subscription(self, subscription_func): ...

    @abc.abstractmethod
    def _process(
            self,
            node: NodeType,
            flags: Set[BaseMiddlewareFlag],
    ) -> PossibleIdentifiers: ...

    @abc.abstractmethod
    def check_context_typ(
            self,
            context_node: NodeType,
    ) -> bool: ...
