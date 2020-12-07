from typing import Dict

from py_type_extractor.type_extractor.nodes.FunctionFound import FunctionFound
from py_type_extractor.type_extractor.nodes.utils.get_self import get_self


def __get_resolver_name(fn_name: str) -> str:
    """
    eg.
    fn_name == 'resolve_something' --> 'something'
    """
    return fn_name[8:]


def __is_resolver_name(fn_name: str) -> bool:
    return fn_name.startswith('resolve_')


def get_raw_resolvers(
        maybe_resolvers: Dict[str, FunctionFound],
) -> Dict[str, FunctionFound]:
    return {
        __get_resolver_name(fn_name): get_self(value)
        for fn_name, value in maybe_resolvers.items()
        if __is_resolver_name(fn_name)
    }