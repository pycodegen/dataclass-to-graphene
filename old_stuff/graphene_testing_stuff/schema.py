import graphene
from fastapi import FastAPI
from starlette.graphql import (
    GraphQLApp
)


class Query(graphene.ObjectType):
    hello = graphene.String(
        name=graphene.String(default_value="hello"),
    )

    goodbye = graphene.String()

    def resolve_hello(self, info, name):
        return f"Hello {name}"

    def resolve_goodbye(self, info):
        return 'See ya!'

schema = graphene.Schema(query=Query)

# we can query for our field (with the default argument)
query_string = '{ hello }'
result = schema.execute(query_string)
print(result.data['hello'])
# "Hello stranger!"

# or passing the argument in the query
query_with_argument = '{ hello(name: "GraphQL") }'
result = schema.execute(
    query_with_argument,
    context={

    },
)
print(result.data['hello'])
# "Hello GraphQL!"