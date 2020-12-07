from codegen.idenfitier.BuiltinIdentifiers import BaseBuiltinIdentifier
from codegen.idenfitier.GeneratedGrapheneObjectIdentifier import GeneratedGrapheneObjectIdentifier
from codegen.idenfitier.ListIdentifier import ListIdentifier
from codegen.idenfitier.OptionalIdentifier import OptionalIdentifier
from codegen.idenfitier.__base__ import BaseIdentifier


# TODO: can be generalized to include `to_original`...
from codegen.middlewares.__codegens__.graphene_typ_def.identifier_to_graphene_typ import naive_ident_to_graphene_typ


def gen_field_convertor_code(
        field_code_str: str,
        # --> string to access the 'field'
        #       eg. 'original.user'
        #
        field_ident: BaseIdentifier,
        func_str: str,  # '_from_original' or '_to_original'
) -> str:
    # hope python gets pattern-matching...
    if isinstance(field_ident, ListIdentifier):
        actual_ident = field_ident.wrapped
        if isinstance(actual_ident, BaseBuiltinIdentifier):
            return field_code_str
        if isinstance(actual_ident, GeneratedGrapheneObjectIdentifier):
            list_dimension = len(field_ident.is_optional_list)
            conversion_func_head = 'map_list(' * list_dimension
            conversion_func_body = f'{naive_ident_to_graphene_typ(actual_ident)}.{func_str}'
            conversion_func_tail = ')' * list_dimension
            conversion_func = \
                conversion_func_head \
                + conversion_func_body \
                + conversion_func_tail
            return f'{conversion_func}({field_code_str})'

    if isinstance(
            field_ident,
            BaseBuiltinIdentifier,
    ) or isinstance(
        field_ident,
        OptionalIdentifier,
    ):
        return field_code_str
    if isinstance(field_ident, GeneratedGrapheneObjectIdentifier):
        return f'{naive_ident_to_graphene_typ(field_ident)}.{func_str}({field_code_str})'
    raise RuntimeError(
        'Could not generate field for Identifier: ',
        field_ident,
    )
