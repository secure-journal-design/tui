from datetime import datetime

from TUI.journal.menu import Menu, Description, Entry
from TUI.journal.models import Journal, Subheading, Body, Title, Topic, Article


class App:
    def __init__(self):
        self.__menu = Menu.Builder(Description('Secure Journal Deisgn'), auto_select=lambda: self.__printArticles()) \
            .with_entry(Entry.create('1', 'Add article')) \
            .with_entry(Entry.create('2', 'Print article')) \
            .with_entry(Entry.create('3', 'Search by topic')) \
            .with_entry(Entry.create('4', 'Sort by newest')) \
            .with_entry(Entry.create('5', 'Sort by oldest')) \
            .with_entry(Entry.create('6', 'Sort by like')) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: print("Bye!"), is_exit=True)) \
            .build()
        self.__journal = Journal()
        test_article = Article(3, 20, datetime.fromtimestamp(1702390272), datetime.fromtimestamp(1702390272),
                               Topic('Computer science'), Title('answer set programming (ASP)'), Body(
                "L'answer set programming (ASP) è una forma di programmazione logica di tipo dichiarativo utilizzato "
                "per problemi di ricerca complessi (in primis NP-difficili), basata sulla semantica del modello "
                "stabile"), 120, Subheading('Answer Set Programming: advanced development'))
        self.__journal.add_article(test_article)

    def __printArticles(self) -> None:
        print_sep = lambda: print('-' * 150)
        print_sep()
        fmt = '%3s %-35.35s %-30.30s %-40.35s %-6s'
        print(fmt % ('#', 'TITLE', 'TOPIC', 'BODY', 'LIKE'))
        print_sep()
        for index in range(self.__journal.articles()):
            article = self.__journal.article(index)
            print(fmt % (index + 1, article.title, article.topic, article.body, article.likes))
        print_sep()

    def run(self):
        self.__menu.run()


def main(name: str):
    if name == '__main__':
        App().run()


main(__name__)
