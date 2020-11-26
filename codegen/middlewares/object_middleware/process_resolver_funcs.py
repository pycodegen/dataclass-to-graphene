from dataclasses import dataclass

from py_type_extractor.type_extractor.nodes.FunctionFound import FunctionFound
from typing import Dict

from codegen.BaseCodegen import BaseCodegen



def get_resolver_name(fn_name: str) -> str:
    """
    eg.
    fn_name == 'resolve_something' --> 'something'
    """
    return fn_name[8:]


def is_resolver_name(fn_name: str) -> bool:
    return fn_name.startswith('resolve_')


@dataclass
class ProcessedResolver:
    pass

def process_resolver_funcs(
        maybe_resolvers: Dict[str, FunctionFound],
        codegen: BaseCodegen,
) -> ProcessedResolver:
    raw_resolvers = {
        get_resolver_name(fn_name): value
        for fn_name, value in maybe_resolvers.items()
        if is_resolver_name(fn_name)
    }