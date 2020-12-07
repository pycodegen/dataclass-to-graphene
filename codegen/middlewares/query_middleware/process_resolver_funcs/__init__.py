from dataclasses import dataclass
from typing import Dict, Set

from codegen.BaseCodegen import BaseCodegen
from codegen.idenfitier import PossibleIdentifiers
from codegen.middleware_flags import BaseMiddlewareFlag, is_input, is_output
from codegen.middlewares.__codegens__.graphene_typ_def.graphene_field_code_from_args_and_output import \
    graphene_field_code_from_args_and_output
from codegen.middlewares.query_middleware.process_resolver_funcs.get_resolver_funcs import get_raw_resolvers
from codegen.middlewares.query_middleware.resolver_fn_impl_code import get_resolver_fn_impl_code


@dataclass
class ResolverFunc:
    name: str
    args_idents: Dict[str, PossibleIdentifiers]
    return_ident: PossibleIdentifiers


class ResolverFuncCodegen:
    resolver_funcs = Dict[str, ResolverFunc]

    def __init__(
            self,
            resolver_funcs: Dict[str, ResolverFunc] = None,
    ):
        self.resolver_funcs = resolver_funcs or dict()

    def add_resolver(
            self,
            name: str,
            args_idents: Dict[str, PossibleIdentifiers],
            return_ident: PossibleIdentifiers,
    ):
        self.resolver_funcs[name] = ResolverFunc(
            name=name,
            args_idents=args_idents,
            return_ident=return_ident,
        )

    def print_code(self):
        code_str = '\n'
        # resolver-fields at the top,
        for name, resolve_fn in self.resolver_funcs.items():

            code_str += graphene_field_code_from_args_and_output(
                args_idents=resolve_fn.args_idents,
                return_ident=resolve_fn.return_ident,
            )
            code_str += '\n'

        #  resolver-impls at the bottom
        for name, resolve_fn in self.resolver_funcs.items():
            code_str += get_resolver_fn_impl_code(
                resolver_name=name,
                args_idents=resolve_fn.args_idents,
                return_ident=resolve_fn.return_ident,
            )
            code_str += '\n'
        return code_str
