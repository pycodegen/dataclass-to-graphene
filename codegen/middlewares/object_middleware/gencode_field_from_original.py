from codegen.idenfitier.BuiltinIdentifiers import BaseBuiltinIdentifier
from codegen.idenfitier.GeneratedGrapheneObjectIdentifier import GeneratedGrapheneObjectIdentifier
from codegen.idenfitier.ListIdentifier import ListIdentifier
from codegen.idenfitier.__base__ import BaseIdentifier


def gencode_field_from_original(
        field_code_str: str,
        # --> string to access the 'field'
        #       eg. 'original.user'
        #
        field_ident: BaseIdentifier,
) -> str:
    """

    """
    if isinstance(field_ident, ListIdentifier):
        actual_ident = field_ident.wrapped
        if isinstance(actual_ident, BaseBuiltinIdentifier):
            return field_code_str
        if isinstance(actual_ident, GeneratedGrapheneObjectIdentifier):
            list_dimension = len(field_ident.is_nullable_list)
            conversion_func_head = 'map_list(' * list_dimension
            conversion_func_body = f'{actual_ident.to_string()}._from_original'
            conversion_func_tail = ')' * list_dimension
            conversion_func = \
                conversion_func_head \
                + conversion_func_body \
                + conversion_func_tail
            return f'{conversion_func}({field_code_str})'
    if isinstance(field_ident, BaseBuiltinIdentifier):
        return field_code_str
    if isinstance(field_ident, GeneratedGrapheneObjectIdentifier):
        return f'{field_ident.to_string()}._from_original({field_code_str})'