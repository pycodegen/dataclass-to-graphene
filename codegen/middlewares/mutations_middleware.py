from typing import Set, Optional

from py_type_extractor.type_extractor.nodes.BaseNodeType import NodeType

from codegen.BaseCodegen import BaseCodegen
from codegen.idenfitier.__base__ import BaseIdentifier
from codegen.middleware_flags import BaseMiddlewareFlag
from codegen.middlewares.__base__ import BaseMiddleware

"""

def add_user(
    user: UserType
) -> Result[Union[ErrorTypes], UserId]


import graphene

class CreatePerson(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    ok = graphene.Boolean()
    person = graphene.Field(lambda: Person)

    def mutate(root, info, name):
        person = Person(name=name)
        ok = True
        return CreatePerson(person=person, ok=ok)

"""


class MutationsMiddleware(BaseMiddleware):
    def process(
            self,
            node: NodeType,
            codegen: BaseCodegen,
            flags: Set[BaseMiddlewareFlag],
    ) -> Optional[BaseIdentifier]:
        pass
