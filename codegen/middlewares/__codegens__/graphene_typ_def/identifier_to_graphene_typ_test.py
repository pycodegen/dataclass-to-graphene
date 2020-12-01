from tabulate import tabulate

from codegen.ModulePath import ModulePath
from codegen.idenfitier.BuiltinIdentifiers import float_identifier, int_identifier
from codegen.idenfitier.IdentifierWithImport import IdentifierWithImport
from codegen.idenfitier.ListIdentifier import ListIdentifier
from codegen.idenfitier.OptionalIdentifier import OptionalIdentifier
from codegen.middlewares.__codegens__.graphene_typ_def import identifier_to_graphene_typ
from utils.lang import strip_margin
from utils.lang.format_code import format_code

if __name__ == '__main__':
    # TODO: make proper tests! (use python ast module)
    print(tabulate([[
        'int',
        identifier_to_graphene_typ(int_identifier),
    ]], tablefmt='grid',
    ))
    print()
    print(tabulate([[
        format_code('List[Optional[List[int]]]'),
        strip_margin('''
        |ListIdent(
        |    is_optional_list: [False, True],
        |    wrapped=int,
        |)
        |'''),
        format_code(
            identifier_to_graphene_typ(ListIdentifier(
                is_optional_list=[False, True],
                wrapped=int_identifier,
            )),
        ),
    ]], tablefmt="grid"))
    print()
    print(tabulate([[
        format_code('List[Optional[Float]]'),
        strip_margin('''
        |ListIdent(
        |    is_optional_list: [False], 
        |    wrapped=OptionalIdentfier[Float],
        |)
        |'''),
        format_code(identifier_to_graphene_typ(ListIdentifier(
            is_optional_list=[False],
            wrapped=OptionalIdentifier(wrapped=float_identifier),
        ))),
    ]], tablefmt="grid"))
    print('')

    print(tabulate([[
        format_code('List[int]'),
        strip_margin("""
        |ListIdent(
        |  is_optional_list=[False],
        |  wrapped=int_identifier,
        |)
        """),
        format_code(
            identifier_to_graphene_typ(
                ListIdentifier(
                    is_optional_list=[False],
                    wrapped=int_identifier,
                )
            ),
        )
    ]], tablefmt="grid"))

    print(tabulate([[
        format_code(strip_margin('''
            |IdentifierWithImport(
            |    module='hello.module',
            |    name='ident_name_here',
            |)
        ''')),
        format_code(identifier_to_graphene_typ(
            IdentifierWithImport(
                module = ModulePath('hello.module'),
                name = 'ident_name_here',
            )
        ))
    ]]))
    print('')

# >>> from tabulate import tabulate
#
# >>> table = [["Sun",696000,1989100000],["Earth",6371,5973.6],
# ...          ["Moon",1737,73.5],["Mars",3390,641.85]]
# >>> print(tabulate(table))
# -----  ------  -------------
# Sun    696000     1.9891e+09
# Earth    6371  5973.6
# Moon     1737    73.5
# Mars     3390   641.85
# -----  ------  -------------


# >>> print(tabulate(table, headers, tablefmt="github"))
# | item   | qty   |
# |--------|-------|
# | spam   | 42    |
# | eggs   | 451   |
# | bacon  | 0     |