from codegen.idenfitier.BuiltinIdentifiers import int_identifier, float_identifier
from codegen.idenfitier.IdentifierWithImport import IdentifierWithImport
from codegen.idenfitier.ListIdentifier import ListIdentifier
from codegen.idenfitier.OptionalIdentifier import OptionalIdentifier
from codegen.idenfitier.__base__ import BaseIdentifier
from utils.lang import strip_margin


def identifier_to_graphene_typ(
        identifier: BaseIdentifier,
        _graphene: str = 'graphene',
) -> str:
    """
    tries to convert python's non-nullable-by-default to graphene's nullable-by-default
    @param identifier: Identifier
    @param _graphene: (not required) only if using `import graphene as`
    @return: graphene-type code string

        ```
        graphene.List(required=False, graphene.Int)
        ```
    """
    if isinstance(
            identifier,
            ListIdentifier,
    ):
        """
        List[Optional[List[int]]]
        --> g.List(
                required=True
                of_type=g.List(
                    required=False
                    of_type=g.List(
                        required=True
                        of_type=g.Int

        List[Optional[int]]
        --> g.List(
                required=True
                of_type=g.g.Int

        """
        actual_ident = identifier.wrapped
        head = ''.join([
            f'{_graphene}.List(required={not is_optional}, of_type='
            for is_optional in identifier.is_optional_list
        ])
        tail = ')' * len(identifier.is_optional_list)
        if not isinstance(actual_ident, OptionalIdentifier):
            actual_ident_typ = __naive_ident_to_graphene_typ(
                identifier=actual_ident,
                _graphene=_graphene,
            )
            return f'{head}{_graphene}.NonNull({actual_ident_typ}){tail}'
        actual_ident_wrapped_typ = __naive_ident_to_graphene_typ(
            identifier=actual_ident.wrapped,
            _graphene=_graphene,
        )
        return f'{head}{actual_ident_wrapped_typ}{tail}'

    if isinstance(
            identifier,
            OptionalIdentifier,
    ):
        return __naive_ident_to_graphene_typ(
            identifier=identifier.wrapped,
            _graphene=_graphene,
        )
    ident_as_is = __naive_ident_to_graphene_typ(
        identifier=identifier,
        _graphene=_graphene,
    )
    return f'{_graphene}.NonNullable({ident_as_is})'


def __naive_ident_to_graphene_typ(
        identifier: BaseIdentifier,
        _graphene: str = 'graphene',
) -> str:
    """
    "naively" converts identifier to graphene-type codestr
    @param identifier:
    @param _graphene:
    @return:
    """
    if isinstance(
            identifier,
            IdentifierWithImport,
    ):
        return f'{identifier.module}.{identifier.name}'
