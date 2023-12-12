import datetime
from dataclasses import dataclass
from typeguard import typechecked
from valid8 import validate

from validation.regex import pattern


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
    subheading: str

    def __post_init__(self):
        validate('body_length', self.body, max_len=1200, min_len=20, custom=pattern(r'[0-9A-Za-zÀ-Ùà-ù ;.,_\-\'\?\!\n]*'))
        validate('title-length', self.title, max_len=60, min_len=5, custom=pattern(r'[0-9A-Za-zÀ-Ùà-ù ;.,_\-\'\?\!\n]*'))
        validate('topic_length', self.topic, max_len=20, min_len=3, custom=pattern(r'[0-9A-Za-zÀ-Ùà-ù -]*'))
        validate('subheading_length', self.subheading, max_len=255, min_len=5, custom=pattern(r'[0-9A-Za-zÀ-Ùà-ù ;.,_\-\'\?\!\n]*'))












