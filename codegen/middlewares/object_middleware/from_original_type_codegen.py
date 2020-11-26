from dataclasses import dataclass, field
from typing import Dict

from codegen.idenfitier.BuiltinIdentifiers import BaseBuiltinIdentifier
from codegen.idenfitier.GeneratedGrapheneObjectIdentifier import GeneratedGrapheneObjectIdentifier
from codegen.idenfitier.ListIdentifier import ListIdentifier
from codegen.idenfitier.__base__ import BaseIdentifier
from utils.lang.strip_margin import strip_margin

"""
generated output:

class SomeGrapheneObject(graphene.Object):
    ... (other things)

    @classmethod
    def _from_original(cls, original):
        return cls(
            user = original.
        )
"""


@dataclass
class FromOriginalTypeCodegen:
    field_codestring_map: Dict[str, str] = field(default_factory=dict)
    original_name = str = 'original'

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
        if isinstance(identifier, ListIdentifier):
            actual_identifier = identifier.wrapped
            if isinstance(actual_identifier, BaseBuiltinIdentifier):
                return f'{self.original_name}.{name}'
            if isinstance(actual_identifier, GeneratedGrapheneObjectIdentifier):
                list_dimension = len(identifier.is_nullable_list)
                conversion_func_head = 'map_list(' * list_dimension
                conversion_func_body = f'{actual_identifier.to_string()}._from_original'
                conversion_func_tail = ')' * list_dimension
                conversion_func = \
                    conversion_func_head \
                    + conversion_func_body \
                    + conversion_func_tail
                return f'{conversion_func}({self.original_name}.{name})'
        if isinstance(identifier, BaseBuiltinIdentifier):
            return f'{self.original_name}.{name}'
        if isinstance(identifier, GeneratedGrapheneObjectIdentifier):
            return f'{identifier.to_string()}._from_original({self.original_name}.{name})'

    def print_code(self):
        body = '\n'.join([
            f'|        {key} = {value}'
            for key, value
            in self.field_codestring_map.items()
        ])

        func_string = strip_margin(f"""
        |@classmethod
        |def _from_original(cls, {self.original_name}):
        |    return cls(
                {body}
        |    )
        """)
        return func_string
