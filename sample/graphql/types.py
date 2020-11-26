from dataclasses import dataclass
from typing import Union


@dataclass
class ImagePostContent:
    image_url: str
    text: str


@dataclass
class LinkPostContent:
    link_url: str


@dataclass
class Post:
    id: int
    title: str
    contents: Union[
        LinkPostContent,
        ImagePostContent,
    ]