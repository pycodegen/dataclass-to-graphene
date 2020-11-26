from dataclasses import dataclass
import strawberry
from typing import (
    Generic, List, TypeVar,
)

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



class UserFriendsField(Resolver[AppContext]):
    def resolve(
        self,
        context: AppContext,

    ) -> List['User']:

        return []

collector.add_resolver(UserFriendsField)

class User:
    name: str
    age: int
    friends: UserFriendsField

# or:

from old_stuff.dataclass_graphene.__callable_protocols import (
    ContextCallable,
)

# TContext = TypeVar('TContext')
TArgs = TypeVar('TArgs')
TResult = TypeVar('TResult')

class TypesBase(Generic[TContext]):

    def add_resolver(
            self,
            resolver: ContextCallable[
                AppContext, TArgs, TResult
            ]) -> ContextCallable[AppContext, TArgs, TResult]:
                return resolver

class AppTypesBase(TypesBase[AppContext]):
    pass

class User2(AppTypesBase):
    name: str
    friends:

