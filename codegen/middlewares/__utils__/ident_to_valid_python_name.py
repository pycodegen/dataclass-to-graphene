from codegen.idenfitier import IdentifierWithImport
from codegen.idenfitier.__base__ import BaseIdentifier


# FIXME: may need more work!
from codegen.middlewares.__codegens__.graphene_typ_def.identifier_to_graphene_typ import naive_ident_to_graphene_typ


def ident_to_valid_python_name(
        ident: IdentifierWithImport,
):
    ident_str = naive_ident_to_graphene_typ(ident)
    # 1. replace '.' to '_'
    return ident_str.replace('.', '_')
