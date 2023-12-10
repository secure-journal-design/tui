import datetime
from dataclasses import dataclass
from valid8 import validate


@dataclass(frozen=True)
class Article:
    article_id: int
    author_id: int
    created_at: datetime
    updated_at: datetime
    topic: str
    title: str
    body: str
    likes: list[str]




