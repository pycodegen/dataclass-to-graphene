import pathlib
from typing import List, Optional, Set, Any, Dict

from py_type_extractor.type_extractor.nodes.BaseNodeType import NodeType
from py_type_extractor.type_extractor.nodes.ClassFound import ClassFound
from py_type_extractor.type_extractor.type_extractor import TypeExtractor

from codegen.BaseCodegen import BaseCodegen
from codegen.GeneratedFile.generated_file_pool import GeneratedFilePool
from codegen.GeneratedFile.writer import write_generated_file_pool
from codegen.ModulePath import ModulePath
from codegen.ModulePath.RootModulePath import RootModulePath
from codegen.errors.ErrorCollector import ErrorCollector
from codegen.extractor_flags import (
    is_mutation_flag,
    is_query_flag,
    is_subscription_flag,
)
from codegen.idenfitier.__base__ import BaseIdentifier
from codegen.middleware_flags.__base__ import BaseMiddlewareFlag
from codegen.middlewares.__base__ import BaseMiddleware
from codegen.middlewares.builtins_middleware import BuiltinsMiddleware
from codegen.middlewares.list_middleware import ListMiddleware
from codegen.middlewares.object_middleware import ObjectMiddleware
from codegen.middlewares.optional_middleware import OptionalMiddleware
from codegen.middlewares.output_union_middleware import OutputUnionMiddleware
from codegen.middlewares.query_middleware import QueryMiddleware


class Codegen(BaseCodegen):
    def __init__(
            self,
            context_cls: Any,
            middlewares: List[BaseMiddleware] = None,
            root_module_path: Optional[RootModulePath] = None,
            error_collector: ErrorCollector = None,
            already_processed: Dict[NodeType, BaseIdentifier] = None,
    ):
        self.type_extractor = TypeExtractor()
        self.error_collector = error_collector or ErrorCollector()
        context_class_found = self.type_extractor.rawtype_to_node(context_cls)
        if not isinstance(context_class_found, ClassFound):
            # TODO: what about generic-class?
            raise RuntimeError('context_cls is not Class')
        self.context_class = context_class_found

        self.root_module_path = root_module_path \
                                or RootModulePath(ModulePath('graphql_generated'))
        self.generated_file_pool: GeneratedFilePool = {}

        self.middlewares = middlewares or [
            BuiltinsMiddleware(),
            ListMiddleware(),
            OptionalMiddleware(),
            QueryMiddleware(
                generated_file_pool=self.generated_file_pool,
                root_module_path=self.root_module_path,
            ),
            ObjectMiddleware(
                generated_file_pool=self.generated_file_pool,
                root_module_path=self.root_module_path,
            ),
            OutputUnionMiddleware(
                generated_file_pool=self.generated_file_pool,
                root_module_path=root_module_path,
            )
        ]
        self.already_processed: Dict[NodeType, BaseIdentifier] = \
            already_processed or dict()
        self._queries_nodes: Set[NodeType] = set()
        self._subscriptions_nodes: Set[NodeType] = set()
        self._mutations_nodes: Set[NodeType] = set()

    def add_subscription(self, subscription_func):
        to_add = self.type_extractor.add({
            is_subscription_flag,
        })(subscription_func)
        self._subscriptions_nodes.add(to_add)

    def add_mutation(self, mutation_func):
        self._mutations_nodes.add(
            self.type_extractor.add({
                is_mutation_flag,
            })(mutation_func)
        )

    def add_query(self, query_func):
        to_add = self.type_extractor.add({
            is_query_flag,
        })(query_func)
        if isinstance(to_add, ClassFound):
            self._queries_nodes\
                .add(to_add.get_self())
        else:
            raise RuntimeError("Query should be class")

    def _process(
            self,
            node: NodeType,
            flags: Set[BaseMiddlewareFlag],
    ) -> BaseIdentifier:
        if node in self.already_processed:
            return self.already_processed[node]
        for middleware in self.middlewares:
            maybe_identifier = middleware.process(
                node=node,
                codegen=self,
                flags=flags,
            )
            if maybe_identifier:
                self.already_processed[node] = maybe_identifier
                return maybe_identifier
        raise RuntimeError('Could not get identifier for: ', node)

    def check_context_typ(
            self,
            context_node: NodeType,
    ) -> bool:
        return context_node == self.context_class

    def process(self):
        for node in self._queries_nodes:
            self._process(node, set())

    def write_files(self, root_folder: pathlib.Path):
        write_generated_file_pool(
            generated_file_pool=self.generated_file_pool,
            root_folder=root_folder,
        )
