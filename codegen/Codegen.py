from typing import List, Optional, Set

from py_type_extractor.type_extractor.nodes.BaseNodeType import NodeType
from py_type_extractor.type_extractor.type_extractor import TypeExtractor

from codegen.BaseCodegen import BaseCodegen
from codegen.GeneratedFile import (
    GeneratedFile, GeneratedQueriesFile,
)
from codegen.GeneratedFile.generated_file_pool import GeneratedFilePool
from codegen.ModulePath import ModulePath
from codegen.GeneratedFile.MutationsModule import GeneratedMutationsFile
from codegen.ModulePath.RootModulePath import RootModulePath
from codegen.extractor_flags.is_mutation import is_mutation_flag
from codegen.extractor_flags.is_query import is_query_flag
from codegen.extractor_flags.is_subscription import is_subscription_flag
from codegen.idenfitier.__base__ import BaseIdentifier
from codegen.middleware_flags.__base__ import BaseMiddlewareFlag
from codegen.middlewares.__base__ import BaseMiddleware
from codegen.middlewares.builtins_middleware import BuiltinsMiddleware
from codegen.middlewares.list_middleware import ListMiddleware
from codegen.middlewares.object_middleware import ObjectMiddleware
from codegen.middlewares.optional_middleware import OptionalMiddleware


class Codegen(BaseCodegen):
    def __init__(
            self,
            middlewares: List[BaseMiddleware] = None,
            root_module_path: Optional[RootModulePath] = None
    ):
        self.type_extractor = TypeExtractor()

        self.root_module_path = root_module_path \
                                or RootModulePath(ModulePath('graphql_generated'))
        self.generated_file_pool: GeneratedFilePool = {}

        self.middlewares = middlewares or [
            BuiltinsMiddleware(),
            ListMiddleware(),
            OptionalMiddleware(),
            ObjectMiddleware(
                generated_file_pool=self.generated_file_pool,
                root_module_path=self.root_module_path,
            ),
        ]

    def add_subscription(self, subscription_func):
        self.type_extractor.add({
            is_subscription_flag,
        })(subscription_func)

    def add_mutation(self, mutation_func):
        self.type_extractor.add({
            is_mutation_flag,
        })(mutation_func)

    def add_query(self, query_func):
        self.type_extractor.add({
            is_query_flag,
        })(query_func)

    def _process(
            self,
            node: NodeType,
            flags: Set[BaseMiddlewareFlag],
    ) -> BaseIdentifier:
        for middleware in self.middlewares:
            maybe_identifier = middleware.process(
                node=node,
                codegen=self,
                flags=flags,
            )
            if maybe_identifier:
                return maybe_identifier
        raise RuntimeError('Could not get identifier for: ', node)
