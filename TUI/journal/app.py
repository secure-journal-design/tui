from datetime import datetime
from typing import Callable, Any, Tuple

import requests
from valid8 import ValidationError, validate

from TUI.journal.menu import Menu, Description, Entry
from TUI.journal.domain import Journal, Subheading, Body, Title, Topic, Article, ID, ArticleToSend, Username, Password, \
    Author

api_server = 'http://localhost:8000/api/v1'


class App:
    __key: str = None

    def __init__(self):
        self.__login()
        self.__menu = Menu.Builder(Description('Secure Journal Design'), auto_select=lambda: self.__printArticles()) \
            .with_entry(Entry.create('1', 'Add article', on_selected=lambda: self.__add_article())) \
            .with_entry(Entry.create('2', 'Print article', on_selected=lambda: self.__print_article())) \
            .with_entry(Entry.create('3', 'Search by topic', on_selected=lambda: self.__search_by_topic())) \
            .with_entry(Entry.create('4', 'Sort by newest', on_selected=lambda: self.__sort_by_newest())) \
            .with_entry(Entry.create('5', 'Sort by oldest', on_selected=lambda: self.__sort_by_oldest())) \
            .with_entry(Entry.create('6', 'Sort by like', on_selected=lambda: self.__sort_by_likes())) \
            .with_entry(Entry.create('7', 'Put like', on_selected=lambda: self.__put_like())) \
            .with_entry(Entry.create('8', 'Refresh', on_selected=lambda: self.__refresh())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: self.__logout(), is_exit=True)) \
            .build()
        self.__journal = Journal()
        self.__loadArticles()

    def __loadArticles(self) -> None:
        res = requests.get(url=f'{api_server}/articles/', headers={'Authorization': f'Token {App.__key}'})
        for article in res.json():
            self.__journal.add_article(Article(article['id'],
                                               Author(article['author']['id'], article['author']['username']),
                                               datetime.strptime(article['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'),
                                               datetime.strptime(article['updated_at'], '%Y-%m-%dT%H:%M:%S.%fZ'),
                                               article['topic'],
                                               article['title'], article['body'], article['num_likes'],
                                               article['subheading']))

    def __printArticles(self) -> None:
        print_sep = lambda: print('-' * 160)
        print_sep()
        fmt = '%-4s %-35.30s %-30.25s %-40.35s %-20.15s  %-20.15s %2s'
        print(fmt % ('#', 'TITLE', 'TOPIC', 'BODY', 'CREATED_AT', 'AUTHOR', 'LIKE'))
        print_sep()

        for index in range(self.__journal.articles()):
            article = self.__journal.article(index)
            print(fmt % (index + 1, article.title, article.topic, article.body, article.created_at.strftime("%d/%m/%Y"),
                         article.author.username, article.likes))
        print_sep()

    def __print_article(self) -> None:
        def builder(value: str) -> int:
            validate('value', int(value), min_value=0, max_value=self.__journal.articles())
            return int(value)

        index = self.__read('Index (0 to cancel): ', builder)
        if index == 0:
            print('Cancelled')
            return
        article = self.__journal.article(index - 1)
        print(f'TITOLO: {article.title}', "\n")
        print(f'TOPIC: {article.topic}', "\n")
        print(f'SUBHEAD: {article.subheading}', "\n")
        print(f'BODY: {article.body}', "\n")
        print()

    @staticmethod
    def __read(prompt: str, builder: Callable) -> Any:
        while True:
            try:
                line = input(f'{prompt}: ')
                res = builder(line.strip())
                return res
            except (TypeError, ValueError, ValidationError) as e:
                print(e)

    @staticmethod
    def __login() -> None:
        while App.__key is None:
            # username = App.__read('Username', Username)
            # pwd = App.__read('Password', Password)
            username = Username("Lorenzo2")
            pwd = Password("Test_234")

            res = requests.post(url=f'{api_server}/auth/login/',
                                data={'username': username.value, 'password': pwd.value})
            if res.status_code == 200:
                json = res.json()
                App.__key = json['key']
            else:
                print(res.json()['non_field_errors'][0])
        print('LOGGED IN')

    @staticmethod
    def __logout() -> None:
        res = requests.post(url=f'{api_server}/auth/logout/', headers={'Authorization': f'Token {App.__key}'})
        if res.status_code == 200:
            print("Logged out!")
        else:
            print("Log out failed")
        print('Bye')

    def run(self) -> None:
        self.__menu.run()

    def __sort_by_oldest(self) -> None:
        self.__journal.sort_by_newest()

    def __sort_by_likes(self) -> None:
        self.__journal.sort_by_like()

    def __sort_by_newest(self) -> None:
        self.__journal.sort_by_oldest()

    def __search_by_topic(self) -> None:
        def builder(value: str) -> int:
            validate('value', int(value), min_value=0, max_value=self.__journal.articles())
            return int(value)

        topic = self.__read('Topic', Topic)
        new_journal = Journal()
        for i in range(self.__journal.articles()):
            if self.__journal.article(i).topic == topic.value:
                new_journal.add_article(self.__journal.article(i))
        self.__journal = new_journal

    def __refresh(self) -> None:
        self.__journal.clear()
        self.__loadArticles()

    def __add_article(self) -> None:
        article = ArticleToSend(*self.__read_article())
        res = requests.post(url=f'{api_server}/articles/editor/', headers={'Authorization': f'Token {App.__key}'},
                            data={"topic": f'{article.topic.value}',
                                  "title": f'{article.title.value}',
                                  "subheading": f'{article.subheading.value}',
                                  "body": f'{article.body.value}',
                                  })
        if res.status_code == 201:
            print('Article added!')
        else:
            print('Error')
        self.__refresh()


    def __read_article(self) -> Tuple[Title, Topic, Subheading, Body]:
        title = self.__read('Title', Title)
        topic = self.__read('Topic', Topic)
        subheading = self.__read('Subheading', Subheading)
        body = self.__read('Body', Body)
        return title, topic, subheading, body

    def __put_like(self) -> None:
        def builder(value: str) -> int:
            validate('value', int(value), min_value=0, max_value=self.__journal.articles())
            return int(value)

        index = self.__read('Index (0 to cancel)', builder)
        if index == 0:
            print('Cancelled')
            return
        article = self.__journal.article(index - 1)
        res = requests.post(url=f'{api_server}/articles/{article.article_id}/like/', headers={'Authorization': f'Token {App.__key}'})
        self.__refresh()


def main(name: str):
    if name == '__main__':
        App().run()


main(__name__)
