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
    subheading = "Pyhton ....."

    article = Article(
        article_id=article_id,
        author_id=author_id,
        created_at=created_at,
        updated_at=updated_at,
        topic=topic,
        title=title,
        body=body,
        likes=likes,
        subheading=subheading
    )


def test_article_body_length():
    wrong_values = ['', 'a', 'AA000bb' * 1000]
    right_values = ['Introduction to Python.', 'A?\'??!' * 100,
                    'Nel mezzo del cammin di nostra vita\nmi ritrovai per una selva oscura,\nché la diritta via era smarrita.']

    article_id = 1
    author_id = 101
    created_at = datetime.now()
    updated_at = datetime.now()
    topic = "Technology"
    title = "Introduction to Python"
    likes = ["user1", "user2"]
    subheading = "Pyhton ......."

    for i in wrong_values:
        with pytest.raises(ValidationError):
            article = Article(
                article_id=article_id,
                author_id=author_id,
                created_at=created_at,
                updated_at=updated_at,
                topic=topic,
                title=title,
                body=i,
                likes=likes,
                subheading=subheading
            )

    for i in right_values:
        article = Article(
            article_id=article_id,
            author_id=author_id,
            created_at=created_at,
            updated_at=updated_at,
            topic=topic,
            title=title,
            body=i,
            likes=likes,
            subheading=subheading
        )


def test_article_title_length():
    wrong_values = ['', 'a', 'AA000bb' * 30]
    right_values = ['Introduction to Python', 'A' * 30,
                    'Nel mezzo del cammin di nostra vita\n']

    article_id = 1
    author_id = 101
    created_at = datetime.now()
    updated_at = datetime.now()
    topic = "Technology"
    body = "Introduction to Python"
    likes = ["user1", "user2"]
    subheading = "Pyhton ......."

    for i in wrong_values:
        with pytest.raises(ValidationError):
            article = Article(
                article_id=article_id,
                author_id=author_id,
                created_at=created_at,
                updated_at=updated_at,
                topic=topic,
                title=i,
                body=body,
                likes=likes,
                subheading=subheading
            )

    for i in right_values:
        article = Article(
            article_id=article_id,
            author_id=author_id,
            created_at=created_at,
            updated_at=updated_at,
            topic=topic,
            title=i,
            body=body,
            likes=likes,
            subheading=subheading
        )


def test_article_topic_length():
    wrong_values = ['', 'a', 'AA000bb' * 1000, 'Sport?!']
    right_values = ['Sci-Fi', 'Sport']

    article_id = 1
    author_id = 101
    created_at = datetime.now()
    updated_at = datetime.now()
    title = "Introduction to Python"
    body = "Python is a versatile programming language..."
    likes = ["user1", "user2"]
    subheading = "Pyhton ......."

    for i in wrong_values:
        with pytest.raises(ValidationError):
            article = Article(
                article_id=article_id,
                author_id=author_id,
                created_at=created_at,
                updated_at=updated_at,
                topic=i,
                title=title,
                body=body,
                likes=likes,
                subheading=subheading
            )

    for i in right_values:
        article = Article(
            article_id=article_id,
            author_id=author_id,
            created_at=created_at,
            updated_at=updated_at,
            topic=i,
            title=title,
            body=body,
            likes=likes,
            subheading=subheading
        )


def test_article_subheading_length():
    wrong_values = ['', 'a', 'AA000bb' * 1000]
    right_values = ['Sci-Fi', 'Sport']

    article_id = 1
    author_id = 101
    created_at = datetime.now()
    updated_at = datetime.now()
    topic = "Technology"
    title = "Introduction to Python"
    body = "Python is a versatile programming language..."
    likes = ["user1", "user2"]

    for i in wrong_values:
        with pytest.raises(ValidationError):
            article = Article(
                article_id=article_id,
                author_id=author_id,
                created_at=created_at,
                updated_at=updated_at,
                topic=topic,
                title=title,
                body=body,
                likes=likes,
                subheading=i
            )

    for i in right_values:
        article = Article(
            article_id=article_id,
            author_id=author_id,
            created_at=created_at,
            updated_at=updated_at,
            topic=topic,
            title=title,
            body=body,
            likes=likes,
            subheading=i
        )