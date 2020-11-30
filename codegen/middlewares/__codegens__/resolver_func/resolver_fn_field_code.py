import textwrap
from typing import Dict

from codegen.idenfitier.BuiltinIdentifiers import int_identifier, float_identifier
from codegen.idenfitier.OptionalIdentifier import OptionalIdentifier
from codegen.idenfitier.__base__ import BaseIdentifier
from codegen.middlewares.__utils__.identifier_to_graphql_type import identifier_to_graphql_type
from utils.lang.strip_margin import strip_margin


def get_resolver_fn_field_code(
        args_idents: Dict[str, BaseIdentifier],
        return_ident: BaseIdentifier,
        _g: str = 'graphene',
) -> str:
    args_codes = {
        arg_name: strip_margin(
            f'''{_g}.Argument(
                |    type_={identifier_to_graphql_type(arg_ident)},
                |)'''
        )
        for arg_name, arg_ident in args_idents.items()
    }
    args_code_str = '\n'.join([
        f"'{arg_name}': {arg_code},"
        for arg_name, arg_code in args_codes.items()
    ])
    return_code_str = identifier_to_graphql_type(return_ident)
    return strip_margin(
        f'''graphene.Field(
            |    type_={return_code_str}, 
            |    args={{
            |{textwrap.indent(args_code_str, '        ')}
            |    }}
            |)
            |''')


if __name__ == '__main__':
    print(
        get_resolver_fn_field_code(
            {
                'some_int': int_identifier,
                'some_optional_int': OptionalIdentifier(wrapped=int_identifier)
            },
            return_ident=float_identifier,
        )
    )