from copy import copy

from py_type_extractor.type_extractor.nodes.NoneNode import none_node
from py_type_extractor.type_extractor.nodes.TypeOR import TypeOR


def is_optional_typeor(node: TypeOR):
    if none_node in node.nodes:
        return True


def typeor_discard_optional(typeor_node: TypeOR):
    nodes = copy(typeor_node.nodes)
    nodes.discard(none_node)
    if len(nodes) == 1:
        return list(nodes)[0]

    return TypeOR(
        nodes=nodes,
        options=typeor_node.options,
    )

if __name__ == '__main__':
    result = typeor_discard_optional(
        TypeOR(
            nodes={int, str, none_node}
        )
    )
    print(result)