from dataclasses import dataclass, field
from typing import Dict

from codegen.idenfitier.BuiltinIdentifiers import int_identifier, float_identifier
from codegen.idenfitier.ListIdentifier import ListIdentifier
from codegen.idenfitier.OptionalIdentifier import OptionalIdentifier
from codegen.idenfitier.__base__ import BaseIdentifier
from codegen.middlewares.object_middleware.identifier_to_graphql_type import identifier_to_graphql_type


@dataclass
class GrapheneFieldsDefCodegen:
    field_codestring_map: Dict[str, str] = field(default_factory=dict)
    g: str = 'graphene'
    def add_field(
            self,
            name: str,
            identifier: BaseIdentifier,
    ):
        self.field_codestring_map[name] = self.__get_codestring(
            name=name,
            identifier=identifier,
        )

    def __get_codestring(
            self,
            name: str,
            identifier: BaseIdentifier,
    ) -> str:
        graphql_type_str = identifier_to_graphql_type(
            identifier=identifier,
        )
        return f'{self.g}.Field({graphql_type_str})'

    def generate_code(self) -> str:
        body = '\n'.join([
            f'{key} = {value}'
            for key, value in self.field_codestring_map.items()
        ])
        return body


if __name__ == '__main__':
    a = GrapheneFieldsDefCodegen()
    a.add_field('int_test', int_identifier)
    a.add_field('list_optional', ListIdentifier(
        is_nullable_list=[True, False],
        wrapped=int_identifier,
    ))

    a.add_field('list_of_optional', ListIdentifier(
        is_nullable_list=[False],
        wrapped=OptionalIdentifier(wrapped=float_identifier),
    ))

    a.add_field('list_of_required', ListIdentifier(
        is_nullable_list=[False],
        wrapped=int_identifier,
    ))
    print(a.generate_code())