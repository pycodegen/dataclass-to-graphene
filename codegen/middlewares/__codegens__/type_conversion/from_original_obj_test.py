from codegen.ModulePath import ModulePath
from codegen.idenfitier import OptionalIdentifier
from codegen.idenfitier.BuiltinIdentifiers import int_identifier
from codegen.idenfitier.GeneratedGrapheneObjectIdentifier import (
    GeneratedGrapheneObjectIdentifier,
)
from codegen.idenfitier.ListIdentifier import ListIdentifier
from codegen.middlewares.__codegens__.type_conversion import (
    FromOriginalObjCodegen,
)
from utils.lang.format_code import format_code

if __name__ == '__main__':
    a = FromOriginalObjCodegen(
        field_codestring_map={
            'a': 'b',
            'aaa': '123',
        },
    )
    print(a.print_code())
    print('\n-------\n')

    b = FromOriginalObjCodegen()
    b.add_field(
        'hello',
        ListIdentifier(
            is_optional_list=[True, False],
            wrapped=GeneratedGrapheneObjectIdentifier(
                module=ModulePath('some.custom_graphene'),
                name='Hello',
            )
        )
    )
    b.add_field(
        'some_optional',
        OptionalIdentifier(
            wrapped=int_identifier,
        )
    )
    print(format_code(b.print_code()))