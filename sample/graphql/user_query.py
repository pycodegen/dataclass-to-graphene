from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from sample.graphql import AppContext
from sample.graphql.AppContext import AppContext
from sample.graphql.types import Post


@dataclass
class User:
    id: int
    name: str
    last_seen: Optional[datetime]
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

    def resolve_posts_search(self, context: AppContext, keyword: str) -> List[Post]:
        return []