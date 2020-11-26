from codegen.idenfitier.BuiltinIdentifiers import int_identifier, float_identifier
from codegen.idenfitier.ListIdentifier import ListIdentifier
from codegen.idenfitier.OptionalIdentifier import OptionalIdentifier
from codegen.idenfitier.__base__ import BaseIdentifier


def identifier_to_graphql_type(
        identifier: BaseIdentifier,
        _graphene: str = 'graphene',
) -> str:
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
            for is_optional in identifier.is_nullable_list
        ])
        tail = ')' * len(identifier.is_nullable_list)
        if not isinstance(actual_ident, OptionalIdentifier):
            return f'{head}{_graphene}.NonNull({actual_ident.to_string()}){tail}'
        return f'{head}{actual_ident.wrapped.to_string()}{tail}'

    if isinstance(
            identifier,
            OptionalIdentifier,
    ):
        return f'{identifier.wrapped.to_string()}'
    return f'{_graphene}.NonNullable({identifier.to_string()})'


if __name__ == '__main__':
    # TODO: make proper tests! (use python ast module)
    print(
        identifier_to_graphql_type(int_identifier)
    )
    print(
        identifier_to_graphql_type(ListIdentifier(
            is_nullable_list=[True, False],
            wrapped=int_identifier,
        ))
    )

    print(
        identifier_to_graphql_type(ListIdentifier(
            is_nullable_list=[False],
            wrapped=OptionalIdentifier(wrapped=float_identifier),
        ))
    )

    print(
        identifier_to_graphql_type(ListIdentifier(
            is_nullable_list=[False],
            wrapped=int_identifier,
        ))
    )