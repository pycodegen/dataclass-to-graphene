from codegen.idenfitier.__base__ import BaseIdentifier


# FIXME: may need more work!
def ident_to_valid_python_name(
        ident: BaseIdentifier,
):
    ident_str = ident.to_string()
    # 1. replace '.' to '_'
    return ident_str.replace('.', '_')
