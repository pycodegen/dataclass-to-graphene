from dataclasses import dataclass
import strawberry
from typing import (
    Generic, List, TypeVar,
)

from py_type_extractor.type_extractor.type_extractor import TypeExtractor

'''
About resolvers --- how to '100% type' following code?
'''
@dataclass
@strawberry.type
class SUser:
    name: str
    age: int

    @strawberry.field
    def friends(self, info) -> List['SUser']:
        ...

@strawberry.type
class SQuery:
    @strawberry.field
    def user(self, info) -> SUser:
        return SUser(name="Patrick", age=100)

'''
something to do instead:

1. define 'type-def' classes
2. generate 2 python parts:
 - "user-side-impl": abstract-base-classes
 -
'''

# `type-def` class example:

TContext = TypeVar('TContext')

class Collector:
    def add_resolver(self, cls):
        pass


collector = Collector()


class Resolver(Generic[TContext]):
    pass

class RequestContext:
    user_id: str

class AppContext:
    request: RequestContext



class UserFriendsResolver(Resolver[AppContext]):
    def resolve(
        self,
        context: AppContext,

    ) -> List['User']:

        return []

collector.add_resolver(UserFriendsResolver)

class User:
    name: str
    age: int
    friends: UserFriendsResolver
