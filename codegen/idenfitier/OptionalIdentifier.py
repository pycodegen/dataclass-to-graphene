from codegen.idenfitier.__base__ import BaseIdentifier, WrappedIdentifier


class OptionalIdentifier(WrappedIdentifier):
    wrapped: BaseIdentifier

    def __init__(
            self,
            wrapped: BaseIdentifier
    ):
        self.wrapped = wrapped
