import datetime
from dataclasses import dataclass, field
from typing import List

from typeguard import typechecked
from valid8 import validate

from TUI.validation.regex import pattern


@typechecked
@dataclass(frozen=True)
class Topic:
    value: str

    def __post_init__(self):
        validate('topic_length', self.value, max_len=20, min_len=3, custom=pattern(r'[0-9A-Za-zÀ-Ùà-ù -]*'))

    def __str__(self):
        return self.value


@typechecked
@dataclass(frozen=True)
class Title:
    value: str

    def __post_init__(self):
        validate('title-length', self.value, max_len=60, min_len=5,
                 custom=pattern(r'[0-9A-Za-zÀ-Ùà-ù ;:.,_\-\'\?\!\n()]*'))

    def __str__(self):
        return self.value


@typechecked
@dataclass(frozen=True)
class Body:
    value: str

    def __post_init__(self):
        validate('body_length', self.value, max_len=1200, min_len=20,
                 custom=pattern(r'[0-9A-Za-zÀ-Ùà-ù ;:.,_\-\'\?\!\n()]*'))

    def __str__(self):
        return self.value


@typechecked
@dataclass(frozen=True)
class Subheading:
    value: str

    def __post_init__(self):
        validate('subheading_length', self.value, max_len=255, min_len=5,
                 custom=pattern(r'[0-9A-Za-zÀ-Ùà-ù ;:.,_\-\'\?\!\n()]*'))

    def __str__(self):
        return self.value


@typechecked
@dataclass(frozen=True)
class Article:
    article_id: int
    author_id: int
    created_at: datetime
    updated_at: datetime
    topic: Topic
    title: Title
    body: Body
    likes: int
    subheading: Subheading


@typechecked
@dataclass(frozen=True)
class Journal:
    __articles: List[Article] = field(default_factory=list, init=False)

    def articles(self) -> int:
        return len(self.__articles)

    def article(self, index: int) -> Article:
        return self.__articles[index]

    def add_article(self, article: Article) -> None:
        self.__articles.append(article)

