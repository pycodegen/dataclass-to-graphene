import abc


class BaseIdentifier(metaclass=abc.ABCMeta):
    pass


class WrappedIdentifier(
    BaseIdentifier,
    metaclass=abc.ABCMeta
):
    wrapped: BaseIdentifier

