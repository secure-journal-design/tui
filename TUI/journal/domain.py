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
class Username:
    value: str

    def __post_init__(self):
        validate('username', self.value, max_len=150, custom=pattern(r'[0-9A-Za-z_@+\-]*'))


@typechecked
@dataclass(frozen=True)
class Password:
    value: str

    def __post_init__(self):
        validate('password', self.value, max_len=150)


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
class ID:
    value: int


@typechecked
@dataclass(frozen=True)
class Author:
    id: ID
    username: Username


@typechecked
@dataclass(frozen=True, order=True)
class Article:
    article_id: ID
    author: Author
    created_at: datetime
    updated_at: datetime
    topic: Topic
    title: Title
    body: Body
    likes: int
    subheading: Subheading


@typechecked
@dataclass(frozen=True)
class ArticleToSend:
    topic: Topic
    title: Title
    subheading: Subheading
    body: Body


@typechecked
@dataclass(frozen=True)
class Journal:
    __articles: List[Article] = field(default_factory=list, init=False)

    def articles(self) -> int:
        return len(self.__articles)

    def article(self, index: int) -> Article:
        validate('index', index, min_value=0, max_value=self.articles() - 1)
        return self.__articles[index]

    def add_article(self, article: Article) -> None:
        self.__articles.append(article)

    def sort_by_newest(self):
        self.__articles.sort(key=lambda x: x.created_at)

    def sort_by_oldest(self):
        self.__articles.sort(key=lambda x: x.created_at, reverse=True)

    def sort_by_like(self):
        self.__articles.sort(key=lambda x: -x.likes)

    def clear(self):
        self.__articles.clear()



