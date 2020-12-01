# from graphene import ObjectType, Field, List, String, Int, Union
#
# mock_data = {
#     "episode": 3,
#     "characters": [
#         {
#             "type": "Droid",
#             "name": "R2-D2",
#             "primaryFunction": "Astromech"
#         },
#         {
#             "type": "Human",
#             "name": "Luke Skywalker",
#             "homePlanet": "Tatooine"
#         },
#         {
#             "type": "Starship",
#             "name": "Millennium Falcon",
#             "length": 35
#         }
#     ]
# }
#
#
# class Human(ObjectType):
#     name = String()
#     homePlanet = String()
#
#
# class Droid(ObjectType):
#     name = String()
#     primaryFunction = String()
#
#
# class Starship(ObjectType):
#     name = String()
#     length = Int()
#
#
# class Character(Union):
#     class Meta:
#        types = (Human, Droid, Starship)
#
#     @classmethod
#     def resolve_type(cls, instance, info):
#         if instance["type"] == "Human":
#             return Human
#         if instance["type"] == "Droid":
#             return Droid
#         if instance["type"] == "Starship":
#             return Starship
#
#
# class RootQuery(ObjectType):
#     result = Field(SearchResult)
#
#     def resolve_result(_, info):
#         return mock_data