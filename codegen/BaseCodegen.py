import abc

from py_type_extractor.type_extractor.nodes.BaseNodeType import NodeType

from codegen.idenfitier.__base__ import BaseIdentifier


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
    ) -> BaseIdentifier:
        ...
