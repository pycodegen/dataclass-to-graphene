from dataclasses import dataclass, field

from typing import Dict

from codegen.idenfitier.ListIdentifier import ListIdentifier
from codegen.idenfitier.OptionalIdentifier import OptionalIdentifier
from codegen.idenfitier.__base__ import BaseIdentifier


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
                f'{self.g}.List(required={is_optional}, of_type='
                for is_optional in identifier.is_nullable_list
            ])
            tail = ')' * len(identifier.is_nullable_list)
            if not isinstance(actual_ident, OptionalIdentifier):
                return f'{head}{self.g}.NonNull({actual_ident.to_string()}){tail}'
            return f'{head}{actual_ident.wrapped.to_string()}{tail}'

        if isinstance(
                identifier,
                OptionalIdentifier,
        ):
            return f'{self.g}.Field(type_={identifier.wrapped.to_string()})'
        return f'{self.g}.Field(required=True, type_={identifier.to_string()})'

    def generate_code(self) -> str:
        pass