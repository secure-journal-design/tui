import pytest
from datetime import datetime
from valid8 import ValidationError

from TUI.journal.domain import Article, Title, Topic, Body, Subheading, ID
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
        Article(ID(1), ID(1), datetime.fromtimestamp(1702390272), datetime.fromtimestamp(1702390272), Topic('Sport'), Title('Title'), Body('Contenuto di poco contenuto'), 125, Subheading('Niente di eccezionale')),
        Article(ID(2), ID(10), datetime.fromtimestamp(1702390272), datetime.fromtimestamp(1702390272), Topic('Fisica'), Title('Quantum computing'), Body('Il quantum computing (o calcolo quantistico) è una tecnologia emergente che sfrutta le leggi della meccanica quantistica per risolvere problemi troppo complessi per i computer classici. '), 11, Subheading("Cos'è Quantum Computing")),
        Article(ID(3), ID(20), datetime.fromtimestamp(1702390272), datetime.fromtimestamp(1702390272), Topic('Computer science'), Title('Answer set programming (ASP)'), Body("L'answer set programming (ASP) è una forma di programmazione logica di tipo dichiarativo utilizzato per problemi di ricerca complessi (in primis NP-difficili), basata sulla semantica del modello stabile"), 120, Subheading('Answer Set Programming: advanced development'))
    ]


def test_article_topic(articles):
    assert articles[0].topic.value == 'Sport'
    assert articles[1].topic.value == 'Fisica'
    assert articles[2].topic.value == 'Computer science'


