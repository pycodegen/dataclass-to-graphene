from dataclasses import dataclass, field
from typing import Dict

from codegen.idenfitier.__base__ import BaseIdentifier
from utils.lang.strip_margin import strip_margin
from .field_from_original import field_from_original

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
class FromOriginalObjCodegen:
    field_codestring_map: Dict[str, str] = field(default_factory=dict)
    _orig = str = 'original'

    def add_field(
            self,
            name: str,
            identifier: BaseIdentifier,
    ):
        self.field_codestring_map[name] = field_from_original(
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
