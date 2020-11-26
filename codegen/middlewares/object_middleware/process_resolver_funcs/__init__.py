from typing import Dict

from py_type_extractor.type_extractor.nodes.FunctionFound import FunctionFound

from codegen.BaseCodegen import BaseCodegen
from codegen.idenfitier.__base__ import BaseIdentifier
from .get_resolver_fn_field_code import get_resolver_fn_field_code
from codegen.middlewares.object_middleware.process_resolver_funcs.get_resolver_fn_impl_code import \
    get_resolver_fn_impl_code


def get_resolver_name(fn_name: str) -> str:
    """
    eg.
    fn_name == 'resolve_something' --> 'something'
    """
    return fn_name[8:]


def is_resolver_name(fn_name: str) -> bool:
    return fn_name.startswith('resolve_')


# TODO: extract out (can be used by subscriptions)


def process_resolver_funcs(
        maybe_resolvers: Dict[str, FunctionFound],
        codegen: BaseCodegen,
):
    raw_resolvers: Dict[str, FunctionFound] = {
        get_resolver_name(fn_name): value
        for fn_name, value in maybe_resolvers.items()
        if is_resolver_name(fn_name)
    }
    for name, raw_resolver in raw_resolvers.items():
        # maybe: get identifiers for resolvers here?
        return_ident = codegen._process(
            raw_resolver.return_type
        )

        # TODO: filter-out 'context' or any other 'special' args
        args_idents: Dict[str, BaseIdentifier] = {
            args_name: codegen._process(args_node)
            for args_name, args_node in raw_resolver.params.items()
        }

        resolver_fn_field_code = get_resolver_fn_field_code(
            args_idents=args_idents,
            return_ident=return_ident,
        )

        resolver_fn_impl_code = get_resolver_fn_impl_code(
            resolver_name=name,
            return_ident=return_ident,
            args_idents=args_idents,
        )
    # return resolver_codes