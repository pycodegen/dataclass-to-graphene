from codegen.ModulePath import ModulePath
from codegen.idenfitier.GeneratedGrapheneObjectIdentifier import (
    GeneratedGrapheneObjectIdentifier,
)
from codegen.idenfitier.ListIdentifier import ListIdentifier
from .from_original_obj import FromOriginalObjCodegen


if __name__ == '__main__':
    a = FromOriginalObjCodegen(
        field_codestring_map={
            'a': 'b',
            'aaa': '123',
        },
    )
    print(a.print_code())
    print('\n\n-------\n\n')

    b = FromOriginalObjCodegen()
    b.add_field(
        'hello',
        ListIdentifier(
            is_nullable_list=[True, False],
            wrapped=GeneratedGrapheneObjectIdentifier(
                module=ModulePath('some.custom_graphene'),
                name='hello',
            )
        )
    )
    print(b.print_code())