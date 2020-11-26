import textwrap
from dataclasses import dataclass

from py_type_extractor.type_extractor.nodes.FunctionFound import FunctionFound
from typing import Dict

from codegen.BaseCodegen import BaseCodegen
from codegen.idenfitier.__base__ import BaseIdentifier
from codegen.middlewares.object_middleware.identifier_to_graphql_type import identifier_to_graphql_type
from utils.lang.strip_margin import strip_margin


def get_resolver_name(fn_name: str) -> str:
    """
    eg.
    fn_name == 'resolve_something' --> 'something'
    """
    return fn_name[8:]


def is_resolver_name(fn_name: str) -> bool:
    return fn_name.startswith('resolve_')



# TODO: extract out (can be used by subscriptions)
def idents_to_field_str_code(
        args_idents: Dict[str, BaseIdentifier],
        return_ident: BaseIdentifier,
        _g: str = 'graphene',
) -> str:
    args_codes = {
        arg_name: f'{_g}.Argument(type_={identifier_to_graphql_type(arg_ident)})'
        for arg_name, arg_ident in args_idents.items()
    }
    args_code_str = '\n'.join([
        f"'{arg_name}': {arg_code},"
        for arg_name, arg_code in args_codes.items()
    ])
    return_code_str = identifier_to_graphql_type(return_ident)
    field_str = strip_margin(f'''graphene.Field(
                                 |    type_={return_code_str}, 
                                 |    args={{
                                 |{textwrap.indent(args_code_str, '        ')}
                                 |    }}
                                 |)
                                 |''')
    return field_str

@dataclass
class ResolverCodes:
    fields_dict: Dict[str, str]
    resolve_funcs: Dict[str, str]
    def add_raw(
            self,
            name: str,
            raw_resolver: FunctionFound,
            codegen: BaseCodegen,
    ):
        return_ident = codegen._process(raw_resolver.return_type)
        args_idents: Dict[str, BaseIdentifier] = {
            args_name: codegen._process(args_node)
            for args_name, args_node in raw_resolver.params.items()
        }
        field_str = idents_to_field_str_code(
            args_idents=args_idents,
            return_ident=return_ident,
        )

        self.fields_dict[name] = field_str



        pass

def process_resolver_funcs(
        maybe_resolvers: Dict[str, FunctionFound],
        codegen: BaseCodegen,
) -> ResolverCodes:
    raw_resolvers: Dict[str, FunctionFound] = {
        get_resolver_name(fn_name): value
        for fn_name, value in maybe_resolvers.items()
        if is_resolver_name(fn_name)
    }
    resolver_codes = ResolverCodes()
    for name, raw_resolver in raw_resolvers.items():
        resolver_codes.add_raw(
            name=name,
            raw_resolver=raw_resolver,
            codegen=codegen,
        )
