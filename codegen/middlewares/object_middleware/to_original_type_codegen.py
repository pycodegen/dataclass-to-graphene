from dataclasses import dataclass, field

from typing import Dict

from codegen.idenfitier.BuiltinIdentifiers import BaseBuiltinIdentifier
from codegen.idenfitier.GeneratedGrapheneObjectIdentifier import GeneratedGrapheneObjectIdentifier
from codegen.idenfitier.IdentifierWithImport import IdentifierWithImport
from codegen.idenfitier.ListIdentifier import ListIdentifier
from codegen.idenfitier.__base__ import BaseIdentifier
from utils.lang.strip_margin import strip_margin

@dataclass
class ToOriginalType:
    original_type_identifier: IdentifierWithImport
    field_codestring_map: Dict[str, str] = field(default_factory=dict)

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
            if isinstance(
                    actual_identifier,
                    BaseBuiltinIdentifier,
            ):
                return f'self.{name}'
            if isinstance(
                actual_identifier,
                GeneratedGrapheneObjectIdentifier,
            ):
                list_dimension = len(identifier.is_nullable_list)
                conversion_func_head = 'map_list(' * list_dimension
                conversion_func_body = f'{actual_identifier.to_string()}._to_original'
                conversion_func_tail = ')' * list_dimension
                conversion_func = \
                    conversion_func_head \
                    + conversion_func_body \
                    + conversion_func_tail
                return f'{conversion_func}(self.{name})'
        if isinstance(identifier, BaseBuiltinIdentifier):
            return f'self.{name}'
        if isinstance(
                identifier,
                GeneratedGrapheneObjectIdentifier,
        ):
            return f'{identifier.to_string()}._to_original(self.{name})'

    def print_code(self):
        body = '\n'.join([
            f'|        {key} = {value}'
            for key, value
            in self.field_codestring_map
        ])
        func_string = strip_margin(f"""
        |def _to_original(self):
        |    return {self.original_type_identifier}(
                  {body}
        |    )
        |""")
        return func_string