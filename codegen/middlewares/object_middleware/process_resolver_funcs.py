import textwrap
from dataclasses import dataclass, field

from py_type_extractor.type_extractor.nodes.FunctionFound import FunctionFound
from typing import Dict

from codegen.BaseCodegen import BaseCodegen
from codegen.idenfitier.BuiltinIdentifiers import BaseBuiltinIdentifier
from codegen.idenfitier.ListIdentifier import ListIdentifier
from codegen.idenfitier.__base__ import BaseIdentifier
from codegen.middlewares.object_middleware.gencode_field_from_original import gencode_field_from_original
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

def gencode_for_return_ident(
        identifier: BaseIdentifier,
        var_name: str = 'raw_return',
) -> str:
    if isinstance(
            identifier,
            ListIdentifier,
    ):
        actual_ident = identifier.wrapped
        if isinstance(
                actual_ident,
                BaseBuiltinIdentifier
        ):


@dataclass
class ResolverCodes:
    fields_dict: Dict[str, str] = field(default_factory=dict)
    resolve_funcs: Dict[str, str] = field(default_factory=dict)

    def add_raw(
            self,
            name: str,
            raw_resolver: FunctionFound,
            codegen: BaseCodegen,
    ):
        # TODO: refactor out into 2 funcs...
        #  maybe:
        #    resolve_func
        #    resolve_field
        return_ident = codegen._process(raw_resolver.return_type)
        # TODO: filter-out 'context' or any other 'special' args
        args_idents: Dict[str, BaseIdentifier] = {
            args_name: codegen._process(args_node)
            for args_name, args_node in raw_resolver.params.items()
        }
        field_str = idents_to_field_str_code(
            args_idents=args_idents,
            return_ident=return_ident,
        )

        self.fields_dict[name] = field_str

        arg_names = '\n'.join(
            [f'{arg_name},'
             for arg_name
             in args_idents.keys()]
        )
        arg_names_assignments = '\n'.join(
            [f'{arg_name}={arg_name}'
             for arg_name
             in args_idents.keys()]
        )
        # _from_original for return_ident...

        return_value_code_str = gencode_field_from_original(
            field_code_str='result_original',
            field_ident=return_ident,
        )
        resolve_func_code = strip_margin(
            f"""
            |def resolve_{name}(
            |        self, info,
            |{textwrap.indent(arg_names, ' ' * 8)}
            |):
            |    original = self._to_original()
            |    context = info.context
            |    result_original = original.resolve_{name}(
            |        context=context,
            |{textwrap.indent(arg_names_assignments, ' ' * 8)}
            |    )
            |    return {return_value_code_str}
            |"""
        )
        self.resolve_funcs[name] = resolve_func_code


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
        # maybe: get identifiers for resolvers here?
        resolver_codes.add_raw(
            name=name,
            raw_resolver=raw_resolver,
            codegen=codegen,
        )
    return resolver_codes