from py_type_extractor.type_extractor.nodes.BaseOption import BaseTempOption


class BaseTempExtractorFlag(BaseTempOption):
    def __init__(self, name: str):
        self.name = name
