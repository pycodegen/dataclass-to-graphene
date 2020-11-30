from py_type_extractor.type_extractor.nodes.BaseOption import BaseTempOption


class IsMutation(BaseTempOption):
    def __hash__(self):
        return hash(IsMutation)


is_mutation_flag = IsMutation()
