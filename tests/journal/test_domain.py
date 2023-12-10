import pytest
from valid8 import ValidationError

from journal.models import Article
from datetime import datetime


def test_article_creation():
    article_id = 1
    author_id = 101
    created_at = datetime.now()
    updated_at = datetime.now()
    topic = "Technology"
    title = "Introduction to Python"
    body = "Python is a versatile programming language..."
    likes = ["user1", "user2"]

    article = Article(
        article_id=article_id,
        author_id=author_id,
        created_at=created_at,
        updated_at=updated_at,
        topic=topic,
        title=title,
        body=body,
        likes=likes
    )


def test_article_body_length():
    article_id = 1
    author_id = 101
    created_at = datetime.now()
    updated_at = datetime.now()
    topic = "Technology"
    title = "Introduction to Python"
    body = "Python" * 2000
    likes = ["user1", "user2"]

    with pytest.raises(ValidationError):
        article = Article(
            article_id=article_id,
            author_id=author_id,
            created_at=created_at,
            updated_at=updated_at,
            topic=topic,
            title=title,
            body=body,
            likes=likes
        )


def test_article_topic_length():
    article_id = 1
    author_id = 101
    created_at = datetime.now()
    updated_at = datetime.now()
    topic = "Technology" * 10
    title = "Introduction to Python"
    body = "Python ....."
    likes = ["user1", "user2"]

    with pytest.raises(ValidationError):
        article = Article(
            article_id=article_id,
            author_id=author_id,
            created_at=created_at,
            updated_at=updated_at,
            topic=topic,
            title=title,
            body=body,
            likes=likes
        )


def test_article_title_length():
    article_id = 1
    author_id = 101
    created_at = datetime.now()
    updated_at = datetime.now()
    topic = "Technology"
    title = "Introduction to Python" * 100
    body = "Python ....."
    likes = ["user1", "user2"]

    with pytest.raises(ValidationError):
        article = Article(
            article_id=article_id,
            author_id=author_id,
            created_at=created_at,
            updated_at=updated_at,
            topic=topic,
            title=title,
            body=body,
            likes=likes
        )
