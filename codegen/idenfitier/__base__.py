import abc


class BaseIdentifier(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def to_string(self) -> str: ...


class WrappedIdentifier(
    BaseIdentifier,
    metaclass=abc.ABCMeta
):
    wrapped: BaseIdentifier
    def to_string(self) -> str:
        raise RuntimeError('to_string() should not be called for wrapped identifier!', self)

