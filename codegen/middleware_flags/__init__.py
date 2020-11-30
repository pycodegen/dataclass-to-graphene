from dataclasses import dataclass

from codegen.middleware_flags.__base__ import BaseMiddlewareFlag


@dataclass
class SimpleMiddlewareFlag(BaseMiddlewareFlag):
    flag_str: str

    def __hash__(self):
        return id(SimpleMiddlewareFlag) \
               + hash(self.flag_str) \
               + 1


is_input = SimpleMiddlewareFlag('IS_INPUT')
is_output = SimpleMiddlewareFlag('IS_OUTPUT')
