from dataclasses import dataclass, field
from typing import Dict

from codegen.idenfitier.__base__ import BaseIdentifier
from codegen.middlewares.object_middleware.gencode_field_from_original import gencode_field_from_original
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
    _orig = str = 'original'

    def add_field(
            self,
            name: str,
            identifier: BaseIdentifier,
    ):
        self.field_codestring_map[name] = gencode_field_from_original(
            field_code_str=f'{self._orig}.{name}',
            field_ident=identifier,
        )


    def print_code(self):
        body = '\n'.join([
            f'|        {key} = {value}'
            for key, value
            in self.field_codestring_map.items()
        ])

        func_string = strip_margin(f"""
        |@classmethod
        |def _from_original(cls, {self._orig}):
        |    return cls(
                {body}
        |    )
        """)
        return func_string
