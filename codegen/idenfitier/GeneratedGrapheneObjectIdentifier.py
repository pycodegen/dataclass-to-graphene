from codegen.idenfitier.IdentifierWithImport import IdentifierWithImport


# has "_to_original_type" and "_from_original_type"
class GeneratedGrapheneObjectIdentifier(IdentifierWithImport):
    def to_string(self) -> str:
        return f'{self.module}.{self.name}'

