from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from sample.graphql import AppContext
from sample.graphql.AppContext import SampleAppContext
from sample.graphql.types import Post


@dataclass
class User:
    id: int
    name: str
    # last_seen: Optional[int]
    # friends_ids: List[int]
    #
    # def resolve_friends(self, context: SampleAppContext) -> List['User']:
    #     return []
    #     # return [
    #     #     User(
    #     #         id=_id,
    #     #         name=str(_id),
    #     #         # friends_ids=[],
    #     #         # last_seen=None,
    #     #     )
    #     #     for _id in self.friends_ids
    #     # ]
    def resolve_posts_search(
            self,
            context: SampleAppContext,
            keyword: str,
    ) -> List[Post]:
        return []