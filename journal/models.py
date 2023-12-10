import datetime
from dataclasses import dataclass
from typeguard import typechecked
from valid8 import validate


@typechecked
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

    def __post_init__(self):
        validate('body_length', self.body, max_len=1200)
        validate('title-length', self.title, max_len=60)
        validate('topic_length', self.topic, max_len=20)











