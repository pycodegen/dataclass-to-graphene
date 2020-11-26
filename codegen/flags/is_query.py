from py_type_extractor.type_extractor.nodes.BaseOption import BaseTempOption


class IsQuery(BaseTempOption):
    def __hash__(self):
        return hash(IsQuery)


is_query_flag = IsQuery()
