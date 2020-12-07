import textwrap
from dataclasses import dataclass, field
from typing import Dict

from codegen.idenfitier import PossibleIdentifiers, OptionalIdentifier
from codegen.idenfitier.BuiltinIdentifiers import BaseBuiltinIdentifier
from codegen.idenfitier.GeneratedGrapheneObjectIdentifier import GeneratedGrapheneObjectIdentifier
from codegen.idenfitier.ListIdentifier import ListIdentifier
from codegen.idenfitier.OriginalObjIdentifier import OriginalObjIdentifier
from codegen.middlewares.__codegens__.graphene_typ_def.identifier_to_graphene_typ import naive_ident_to_graphene_typ
from codegen.middlewares.__codegens__.type_conversion import gen_field_convertor_code
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
        self.field_codestring_map[name] = gen_field_convertor_code(
            field_code_str=f'self.{name}',
            field_ident=identifier,
            func_str='_to_original'
        )

    def print_code(self):
        body = '\n'.join([
            f'{key}={value},'
            for key, value
            in self.field_codestring_map.items()
        ])
        # TODO: maybe use something else below?
        original_typ_name = f'{self.original_type_identifier.module}.{self.original_type_identifier.name}'
        func_string = strip_margin(f"""
        |def _to_original(self):
        |    return {original_typ_name}(
        |{textwrap.indent(body, ' ' * 8)}
        |    )
        |""")
        return func_string
