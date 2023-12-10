from journal.models import Article
import datetime


def test_article_format():
    article = Article(1234, 2345, datetime.datetime(day=300, month=2, year=2023),
                      datetime.datetime(day=300, month=2, year=2023),
                      'asdfdsasdf', 'sport', 'rsgsegrsg', ['franco', 'giovanni'])
    assert article is not None
