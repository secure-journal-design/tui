import pytest
from datetime import datetime
from valid8 import ValidationError

from TUI.journal.domain import Article, Title, Topic, Body, Subheading, ID, Journal, Author, Username
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
        Article(ID(1), Author(ID(1), Username("Lorenzo")), datetime.fromtimestamp(1102390272), datetime.fromtimestamp(1702390272), Topic('Sport'),
                Title('Title'), Body('Contenuto di poco contenuto'), 125, Subheading('Niente di eccezionale')),
        Article(ID(2), Author(ID(10), Username("Franco1980")), datetime.fromtimestamp(1434390272), datetime.fromtimestamp(1702390272), Topic('Fisica'),
                Title('Quantum computing'), Body(
                'Il quantum computing (o calcolo quantistico) è una tecnologia emergente che sfrutta le leggi della meccanica quantistica per risolvere problemi troppo complessi per i computer classici. '),
                11, Subheading("Cos'è Quantum Computing")),
        Article(ID(3), Author(ID(20), Username("Ricca10")), datetime.fromtimestamp(1662390272), datetime.fromtimestamp(1702390272),
                Topic('Computer science'), Title('Answer set programming (ASP)'), Body(
                "L'answer set programming (ASP) è una forma di programmazione logica di tipo dichiarativo utilizzato per problemi di ricerca complessi (in primis NP-difficili), basata sulla semantica del modello stabile"),
                120, Subheading('Answer Set Programming: advanced development'))
    ]


def test_article_topic(articles):
    assert articles[0].topic.value == 'Sport'
    assert articles[1].topic.value == 'Fisica'
    assert articles[2].topic.value == 'Computer science'


def test_journal_articles(articles):
    journal = Journal()
    for article in articles:
        journal.add_article(article)
    assert journal.articles() == len(articles)


def test_journal_article(articles):
    journal = Journal()
    for i in range(len(articles)):
        journal.add_article(articles[i])
        assert journal.article(i) == articles[i]


def test_journal_sort_by_newest(articles):
    journal = Journal()
    for article in articles:
        journal.add_article(article)
    journal.sort_by_newest()
    for i in range(1, len(articles) - 1):
        assert journal.article(i - 1).created_at <= journal.article(i).created_at


def test_journal_sort_by_oldest(articles):
    journal = Journal()
    for article in articles:
        journal.add_article(article)
    journal.sort_by_oldest()
    for i in range(1, len(articles) - 1):
        assert journal.article(i - 1).created_at >= journal.article(i).created_at


def test_journal_sort_by_like(articles):
    journal = Journal()
    for article in articles:
        journal.add_article(article)
    journal.sort_by_like()
    for i in range(1, len(articles) - 1):
        assert journal.article(i - 1).likes >= journal.article(i).likes


def test_journal_clear(articles):
    journal = Journal()
    for article in articles:
        journal.add_article(article)

    assert journal.articles() == len(articles)
    journal.clear()
    assert journal.articles() == 0
