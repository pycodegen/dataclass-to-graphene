

import textwrap
from typing import Dict

from codegen.idenfitier import PossibleIdentifiers
from codegen.idenfitier.BuiltinIdentifiers import int_identifier, float_identifier
from codegen.idenfitier.OptionalIdentifier import OptionalIdentifier
from codegen.middlewares.__codegens__.graphene_typ_def.identifier_to_graphene_typ import (
    identifier_to_graphene_typ,
)
from utils.lang.strip_margin import strip_margin

"""
common for Subscriptions + Queries!

eg.
`subscribe_todos(self, info, todo_filter: ..)`
`resolve_todos(self, info, todo_filter: ...)`

both require graphene field:

`todos = graphene.Field( type_: TimeOfDay, args: { ... } )`
         -----------------------------------------------
                      |
                      ----- graphene_field_code_from_args_and_output
"""


def graphene_field_code_from_args_and_output(
        args_idents: Dict[str, PossibleIdentifiers],
        return_ident: PossibleIdentifiers,
        _g: str = 'graphene',
) -> str:
    args_codes = {
        arg_name: strip_margin(
            f'''{_g}.Argument(
                |    type_={identifier_to_graphene_typ(arg_ident)},
                |)'''
        )
        for arg_name, arg_ident in args_idents.items()
    }
    args_code_str = '\n'.join([
        f"'{arg_name}': {arg_code},"
        for arg_name, arg_code in args_codes.items()
    ])
    return_code_str = identifier_to_graphene_typ(return_ident)
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
        graphene_field_code_from_args_and_output(
            {
                'some_int': int_identifier,
                'some_optional_int': OptionalIdentifier(wrapped=int_identifier)
            },
            return_ident=float_identifier,
        )
    )