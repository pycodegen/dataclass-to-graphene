'''
what if: we can follow Graphene more closely? (" TypedGraphene" ) ?
 - probably can do "build-time (codegen-time)" "compiler errors" ?




'''
from dataclasses import dataclass
from typing import List, Optional, cast

import graphene as _g


class AppContext:
    pass

## INPUT to codegen
@dataclass
class User:
    id: int
    name: str
    friends_ids: List[int]

    def resolve_friends(self, context: AppContext) -> List['User']:
        return [
            User(
                id=_id,
                name=str(_id),
                friends_ids=[]
            )
            for _id in self.friends_ids
        ]

    def resolve_posts_search(self, context: AppContext, keyword: str) -> List[str]:
        return ['got', 'keyword', keyword]

## OUTPUT from codegen

class G_User(_g.ObjectType):
    __original = User
    id = _g.Field(type_=_g.Int, required=True)
    name = _g.Field(type_=_g.String, required=True)
    friends_ids = _g.List(
        of_type=_g.Int,
    )

    friends = _g.Field(
        type_=_g.List['G_User'],
    )

    def resolve_friends(self, info):
        context = info.context
        friends = self.__original.resolve_friends(cast(User, self), context)
        return [self.__from_original(i) for i in friends]

    posts_search = _g.Field(
        type_=_g.List[_g.String],
        args={
            'keyword': _g.Field(_g.String, required=True),
        },
    )

    def resolve_posts_search(
            self, info,
            keyword,
    ):
        context = info.context
        self.__original.resolve_friends(cast(User, self), context)

    @classmethod
    def __from_original(cls, original: User):
        g_user = cls(
            id=original.id,
            name=original.name,
            friends_ids=original.friends_ids,  # maybe need to convert original-type --> graphene-type here?
        )
        g_user.__original__ = original
        return g_user

## Testing...



_g.Schema()