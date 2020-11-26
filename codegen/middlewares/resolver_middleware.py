# from typing import Optional, Set
#
# from py_type_extractor.type_extractor.nodes.BaseNodeType import NodeType
# from py_type_extractor.type_extractor.nodes.FunctionFound import FunctionFound
# from py_type_extractor.type_extractor.nodes.__flags import FromMethod
#
# from codegen.BaseCodegen import BaseCodegen
# from codegen.flags.__base__ import BaseFlag
# from codegen.flags.is_resolver import get_resolver_flags, is_resolver_flag
#
# from codegen.idenfitier.__base__ import BaseIdentifier
# from codegen.middlewares.__base__ import BaseMiddleware
# from codegen.middlewares.object_middleware import get_resolver_name
#
#
# class ResolverMiddleware(BaseMiddleware):
#     def process(
#             self,
#             node: NodeType,
#             codegen: BaseCodegen,
#             flags: Optional[Set[BaseFlag]],
#     ) -> Optional[BaseIdentifier]:
#         if not isinstance(node, FunctionFound):
#             return None
#         if is_resolver_flag not in flags:
#             return None
#         method_names = [
#             a.method_name for a in node.options if isinstance(a, FromMethod)
#         ]
#         if len(method_names) == 0 or len(method_names) > 1:
#             raise RuntimeError(
#                 f"got resolver flag, but len(method_names) == ",
#                 len(method_names),
#                 "\n - methods: ", method_names)
#         method_name = method_names[0]
#         resolver_name = get_resolver_name(method_name)
#
#         # TODO ?
#
#         '''
#         Q. why not process 'resolver' inside object-middleware ? (type already known / etc etc)
#         '''
#
