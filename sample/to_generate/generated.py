from typing import cast

import graphene as graphene
import sample.graphql.user_query


class User(graphene.ObjectType):
    __original = sample.graphql.User
    id = graphene.Field(
        type_=graphene.Int,
        required=True,
    )
    name = graphene.Field(
        type_=graphene.String, required=True)
    friends_ids = graphene.List(
        of_type=graphene.Int,
    )

    friends = graphene.Field(
        type_=graphene.List['G_User'],
    )

    def resolve_friends(self, info):
        original = User.__to_original(self)

        resolved_raw = original.resolve_friends(info.context)

        # context = info.context
        # friends = self.__original.resolve_friends(cast(User, self), context)
        # return [self.__from_original(i) for i in friends]

    posts_search = graphene.Field(
        type_=graphene.List[graphene.String],
        args={
            'keyword': graphene.Field(graphene.String, required=True),
        },
    )

    @classmethod
    def __from_original(cls, original: sample.graphql.user_query.User):
        g_user = cls(
            id=original.id,
            name=original.name,
            friends_ids=original.friends_ids,  # maybe need to convert original-type --> graphene-type here?
        )
        g_user.__original__ = original
        return g_user

    @classmethod
    def __to_original(cls, self) -> sample.graphql.user_query.User:
        return sample.graphql.user_query.User(
            id=self.id,
            name=self.name,
            friends_ids=self.friends_ids,  # type: ignore
            last_seen=None,
        )

    def resolve_posts_search(
            self, info,
            keyword,
    ):
        context = info.context
        self.__original.resolve_friends(cast(User, self), context)



## Testing...



graphene.Schema()
