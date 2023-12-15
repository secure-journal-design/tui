from datetime import datetime
from typing import Callable, Any, Tuple

import requests
from valid8 import ValidationError, validate

from TUI.journal.menu import Menu, Description, Entry
from TUI.journal.domain import Journal, Subheading, Body, Title, Topic, Article, ID, ArticleToSend

api_server = 'http://localhost:8000/api/v1'


class App:
    __key: str = None
    __csrftoken: str = None

    def __init__(self):
        self.__login()
        self.__menu = Menu.Builder(Description('Secure Journal Design'), auto_select=lambda: self.__printArticles()) \
            .with_entry(Entry.create('1', 'Add article', on_selected=lambda: self.__add_article())) \
            .with_entry(Entry.create('2', 'Print article', on_selected=lambda: self.__print_article())) \
            .with_entry(Entry.create('3', 'Search by topic', on_selected=lambda: self.__search_by_topic())) \
            .with_entry(Entry.create('4', 'Sort by newest', on_selected=lambda: self.__sort_by_newest())) \
            .with_entry(Entry.create('5', 'Sort by oldest', on_selected=lambda: self.__sort_by_oldest())) \
            .with_entry(Entry.create('6', 'Sort by like', on_selected=lambda: self.__sort_by_likes())) \
            .with_entry(Entry.create('7', 'Refresh', on_selected=lambda: self.__refresh())) \
            .with_entry(Entry.create('0', 'Exit', on_selected=lambda: self.__logout(), is_exit=True)) \
            .build()
        self.__journal = Journal()
        self.__loadArticles()

    def __loadArticles(self):
        res = requests.get(url=f'{api_server}/articles/', headers={'Authorization': f'Token {App.__key}'}, cookies={'sessionid':f'{App.__key}', 'csrftoken': f'{App.__csrftoken}'})
        for article in res.json():
            self.__journal.add_article(Article(article['id'],
                                               article['author']['id'],
                                               datetime.strptime(article['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'),
                                               datetime.strptime(article['updated_at'], '%Y-%m-%dT%H:%M:%S.%fZ'),
                                               article['topic'],
                                               article['title'], article['body'], article['num_likes'],
                                               article['subheading']))

    def __printArticles(self) -> None:
        print_sep = lambda: print('-' * 150)
        print_sep()
        fmt = '%3s %-35.35s %-30.30s %-40.35s %-20.20s %-2s'
        print(fmt % ('#', 'TITLE', 'TOPIC', 'BODY', 'CREATED_AT', 'LIKE'))
        print_sep()

        for index in range(self.__journal.articles()):
            article = self.__journal.article(index)
            print(fmt % (index + 1, article.title, article.topic, article.body, article.created_at.strftime("%d/%m/%Y"), article.likes))
        print_sep()

    def __print_article(self):
        def builder(value: str) -> int:
            validate('value', int(value), min_value=0, max_value=self.__journal.articles())
            return int(value)

        index = self.__read('Index (0 to cancel): ', builder)
        if index == 0:
            print('Cancelled')
            return
        article = self.__journal.article(index-1)
        print(f'TITOLO: {article.title}', "\n")
        print(f'TOPIC: {article.topic}', "\n")
        print(f'SUBHEAD: {article.subheading}', "\n")
        for i in range(len(article.body)):
            print(article.body[i], end="")
            if i % 100 == 0 and i != 0:
                print()
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
    def __login():
        while App.__key is None:
            # username = input("Username: ").strip()
            # pwd = input("Password: ").strip()
            username = "Lorenzo2"
            pwd = "Test_234"

            res = requests.post(url=f'{api_server}/auth/login/', data={'username': username, 'password': pwd})
            if res.status_code == 200:
                json = res.json()
                App.__key = json['key']
                print(res.cookies['csrftoken'])
                App.__csrftoken = res.cookies['csrftoken']
            else:
                print(res.json()['non_field_errors'][0])

    @staticmethod
    def __logout():
        res = requests.post(url=f'{api_server}/auth/logout/', headers={'Authorization': f'Token {App.__key}'})
        if res.status_code == 200:
            print("Logged out!")
        else:
            print("Log out failed")
        print('Bye')

    def run(self):
        self.__menu.run()

    def __sort_by_oldest(self):
        self.__journal.sort_by_newest()

    def __sort_by_likes(self):
        self.__journal.sort_by_like()

    def __sort_by_newest(self):
        self.__journal.sort_by_oldest()

    def __search_by_topic(self):
        def builder(value: str) -> int:
            validate('value', int(value), min_value=0, max_value=self.__journal.articles())
            return int(value)

        topic = self.__read('Topic', Topic)
        new_journal = Journal()
        for i in range(self.__journal.articles()):
            if self.__journal.article(i).topic == topic.value:
                new_journal.add_article(self.__journal.article(i))
        self.__journal = new_journal


    def __refresh(self):
        self.__journal.clear()
        self.__loadArticles()

    def __add_article(self):
        article = ArticleToSend(*self.__read_article())
        res = requests.post(url=f'{api_server}/articles/editor/', headers={'Authorization': f'Token {App.__key}'}, data={"topic": article.topic.value,
                                                                                                                         "title": article.title.value,
                                                                                                                         "subheading": article.subheading.value,
                                                                                                                         "body": article.body.value,
                                                                                                                         })
        print(res)
        print('Article added!')


    def __read_article(self) -> Tuple[Title, Topic, Subheading, Body]:
        title = self.__read('Title', Title)
        topic = self.__read('Topic', Topic)
        subheading = self.__read('Subheading', Subheading)
        body = self.__read('Body', Body)
        return title, topic, subheading, body





def main(name: str):
    if name == '__main__':
        App().run()


main(__name__)
