import textwrap
from typing import Dict

from codegen.idenfitier.BuiltinIdentifiers import int_identifier, float_identifier
from codegen.idenfitier.ListIdentifier import ListIdentifier
from codegen.idenfitier.OptionalIdentifier import OptionalIdentifier
from codegen.idenfitier.__base__ import BaseIdentifier
from codegen.middlewares.object_middleware.gencode_field_from_original import gencode_field_from_original
from utils.lang.strip_margin import strip_margin


def get_resolver_fn_impl_code(
        resolver_name: str,
        return_ident: BaseIdentifier,
        args_idents: Dict[str, BaseIdentifier],
):
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
    return strip_margin(
        f"""
        |def resolve_{resolver_name}(
        |        self, info,
        |{textwrap.indent(arg_names, ' ' * 8)}
        |):
        |    original = self._to_original()
        |    context = info.context
        |    result_original = original.resolve_{resolver_name}(
        |        context=context,
        |{textwrap.indent(arg_names_assignments, ' ' * 8)}
        |    )
        |    return {return_value_code_str}
        |"""
    )


if __name__ == '__main__':
    print(get_resolver_fn_impl_code(
        resolver_name='resolved_field_name',
        return_ident=OptionalIdentifier(wrapped=int_identifier),
        args_idents={
            'hello': ListIdentifier(
                is_nullable_list=[True, False],
                wrapped=float_identifier,
            )
        },
    ))