import pytest
from datetime import datetime
from valid8 import ValidationError

from TUI.journal.models import Article, Title, Topic, Body, Subheading
from datetime import datetime


def test_topic():
    wrong_values = ['', 'AB', 'A?', 'ABC??' * 10]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Topic(value)

    correct_values = ['ABC', 'Sport', 'ASP', 'Neural Networks']
    for value in correct_values:
        assert Topic(value).value == value


def test_body():
    wrong_values = ['', 'AB', 'A?', 'Nel mezzo del cammin di nostra vita' * 100]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Body(value)

    correct_values = ['Nel mezzo del cammin di nostra vita\n'
                      'mi ritrovai per una selva oscura,\n'
                      'ché la diritta via era smarrita.',
                      'Ahi quanto a dir qual era è cosa dura\n'
                      'esta selva selvaggia e aspra e forte\n'
                      'che nel pensier rinova la paura!']
    for value in correct_values:
        assert Body(value).value == value


def test_title():
    wrong_values = ['', 'AB', 'A?', 'ABC??' * 100]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Title(value)

    correct_values = ['Python 3.11', 'Neural Networks']
    for value in correct_values:
        assert Title(value).value == value


def test_subheading():
    wrong_values = ['', 'AB', 'A?', 'ABC??' * 100]
    for value in wrong_values:
        with pytest.raises(ValidationError):
            Subheading(value)

    correct_values = ['Nel mezzo del cammin di nostra vita\n', 'Neural Networks']
    for value in correct_values:
        assert Subheading(value).value == value


@pytest.fixture()
def articles():
    return [
        Article(1, 1, datetime.fromtimestamp(1702390272), datetime.fromtimestamp(1702390272), Topic('Sport'), Title('Title'), Body('Contenuto di poco contenuto'), 125, Subheading('Niente di eccezionale')),
        Article(2, 10, datetime.fromtimestamp(1702390272), datetime.fromtimestamp(1702390272), Topic('Fisica'), Title('Quantum computing'), Body('Il quantum computing (o calcolo quantistico) è una tecnologia emergente che sfrutta le leggi della meccanica quantistica per risolvere problemi troppo complessi per i computer classici. '), 11, Subheading("Cos'è Quantum Computing")),
        Article(3, 20, datetime.fromtimestamp(1702390272), datetime.fromtimestamp(1702390272), Topic('Computer science'), Title('answer set programming (ASP)'), Body("L'answer set programming (ASP) è una forma di programmazione logica di tipo dichiarativo utilizzato per problemi di ricerca complessi (in primis NP-difficili), basata sulla semantica del modello stabile"), 120, Subheading('Answer Set Programming: advanced development'))
    ]

def test_article_topic(articles):
    assert articles[0].topic.value == 'Sport'
    assert articles[1].topic.value == 'Fisica'
    assert articles[2].topic.value == 'Computer science'


# def test_article_body_length():
#     wrong_values = ['', 'a', 'AA000bb' * 1000]
#     right_values = ['Introduction to Python.', 'A?\'??!' * 100,
#                     'Nel mezzo del cammin di nostra vita\nmi ritrovai per una selva oscura,\nché la diritta via era smarrita.']
#
#     article_id = 1
#     author_id = 101
#     created_at = datetime.now()
#     updated_at = datetime.now()
#     topic = "Technology"
#     title = "Introduction to Python"
#     likes = ["user1", "user2"]
#     subheading = "Pyhton ......."
#
#     for i in wrong_values:
#         with pytest.raises(ValidationError):
#             article = Article(
#                 article_id=article_id,
#                 author_id=author_id,
#                 created_at=created_at,
#                 updated_at=updated_at,
#                 topic=topic,
#                 title=title,
#                 body=i,
#                 likes=likes,
#                 subheading=subheading
#             )
#
#     for i in right_values:
#         article = Article(
#             article_id=article_id,
#             author_id=author_id,
#             created_at=created_at,
#             updated_at=updated_at,
#             topic=topic,
#             title=title,
#             body=i,
#             likes=likes,
#             subheading=subheading
#         )
#
#
# def test_article_title_length():
#     wrong_values = ['', 'a', 'AA000bb' * 30]
#     right_values = ['Introduction to Python', 'A' * 30,
#                     'Nel mezzo del cammin di nostra vita\n']
#
#     article_id = 1
#     author_id = 101
#     created_at = datetime.now()
#     updated_at = datetime.now()
#     topic = "Technology"
#     body = "Introduction to Python"
#     likes = ["user1", "user2"]
#     subheading = "Pyhton ......."
#
#     for i in wrong_values:
#         with pytest.raises(ValidationError):
#             article = Article(
#                 article_id=article_id,
#                 author_id=author_id,
#                 created_at=created_at,
#                 updated_at=updated_at,
#                 topic=topic,
#                 title=i,
#                 body=body,
#                 likes=likes,
#                 subheading=subheading
#             )
#
#     for i in right_values:
#         article = Article(
#             article_id=article_id,
#             author_id=author_id,
#             created_at=created_at,
#             updated_at=updated_at,
#             topic=topic,
#             title=i,
#             body=body,
#             likes=likes,
#             subheading=subheading
#         )
#
#
# def test_article_topic_length():
#     wrong_values = ['', 'a', 'AA000bb' * 1000, 'Sport?!']
#     right_values = ['Sci-Fi', 'Sport']
#
#     article_id = 1
#     author_id = 101
#     created_at = datetime.now()
#     updated_at = datetime.now()
#     title = "Introduction to Python"
#     body = "Python is a versatile programming language..."
#     likes = ["user1", "user2"]
#     subheading = "Pyhton ......."
#
#     for i in wrong_values:
#         with pytest.raises(ValidationError):
#             article = Article(
#                 article_id=article_id,
#                 author_id=author_id,
#                 created_at=created_at,
#                 updated_at=updated_at,
#                 topic=i,
#                 title=title,
#                 body=body,
#                 likes=likes,
#                 subheading=subheading
#             )
#
#     for i in right_values:
#         article = Article(
#             article_id=article_id,
#             author_id=author_id,
#             created_at=created_at,
#             updated_at=updated_at,
#             topic=i,
#             title=title,
#             body=body,
#             likes=likes,
#             subheading=subheading
#         )
#
#
# def test_article_subheading_length():
#     wrong_values = ['', 'a', 'AA000bb' * 1000]
#     right_values = ['Sci-Fi', 'Sport']
#
#     article_id = 1
#     author_id = 101
#     created_at = datetime.now()
#     updated_at = datetime.now()
#     topic = "Technology"
#     title = "Introduction to Python"
#     body = "Python is a versatile programming language..."
#     likes = ["user1", "user2"]
#
#     for i in wrong_values:
#         with pytest.raises(ValidationError):
#             article = Article(
#                 article_id=article_id,
#                 author_id=author_id,
#                 created_at=created_at,
#                 updated_at=updated_at,
#                 topic=topic,
#                 title=title,
#                 body=body,
#                 likes=likes,
#                 subheading=i
#             )
#
#     for i in right_values:
#         article = Article(
#             article_id=article_id,
#             author_id=author_id,
#             created_at=created_at,
#             updated_at=updated_at,
#             topic=topic,
#             title=title,
#             body=body,
#             likes=likes,
#             subheading=i
#         )
