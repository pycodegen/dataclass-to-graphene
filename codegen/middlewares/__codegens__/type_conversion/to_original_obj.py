import textwrap
from dataclasses import dataclass, field
from typing import Dict

from codegen.idenfitier import PossibleIdentifiers
from codegen.idenfitier.BuiltinIdentifiers import BaseBuiltinIdentifier
from codegen.idenfitier.GeneratedGrapheneObjectIdentifier import GeneratedGrapheneObjectIdentifier
from codegen.idenfitier.ListIdentifier import ListIdentifier
from codegen.idenfitier.OriginalObjIdentifier import OriginalObjIdentifier
from codegen.middlewares.__codegens__.graphene_typ_def.identifier_to_graphene_typ import naive_ident_to_graphene_typ
from utils.lang.strip_margin import strip_margin


@dataclass
class ToOriginalObjCodegen:
    original_type_identifier: OriginalObjIdentifier
    field_codestring_map: Dict[str, str] = field(default_factory=dict)

    def add_field(
            self,
            name: str,
            identifier: PossibleIdentifiers,
    ):
        self.field_codestring_map[name] = self.__get_codestring(
            name=name,
            identifier=identifier,
        )

    def __get_codestring(
            self,
            name: str,
            identifier: PossibleIdentifiers,
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
                list_dimension = len(identifier.is_optional_list)
                conversion_func_head = 'map_list(' * list_dimension
                conversion_func_body = f'{naive_ident_to_graphene_typ(actual_identifier)}._to_original'
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
            return f'{naive_ident_to_graphene_typ(identifier)}._to_original(self.{name})'
        raise RuntimeError('__get_codestring failed for ', identifier)

    def print_code(self):
        body = '\n'.join([
            f'{key} = {value}'
            for key, value
            in self.field_codestring_map
        ])
        func_string = strip_margin(f"""
        |def _to_original(self):
        |    return {self.original_type_identifier}(
        |{textwrap.indent(body, ' ' * 8)}
        |    )
        |""")
        return func_string
