from typing import List

from thinking.two_phase_build.original.__base__ import Resolver


class Posts:
    id: str
    title: str


class User:
    name: str
    posts: Resolver[None, List[Posts]]
