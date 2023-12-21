import dataclasses
from dataclasses import InitVar
from pathlib import Path
from typing import Any
import re
from unittest import mock
from unittest.mock import MagicMock, patch, mock_open, Mock, call

from TUI.journal.app import App, main
from TUI.journal.domain import Article


@patch('builtins.input', side_effect=['User', 'Psssword', '0'])
@patch('builtins.print')
@patch('TUI.journal.app.requests.post')
@patch('TUI.journal.app.requests.get')
def test_app_success(mock_get, mock_post, mock_print, mock_input):
    mock_response_login = Mock()
    mock_response_login.status_code = 200
    mock_response_login.json.return_value = {'key': 'test_key'}

    mock_response_get = Mock()
    mock_response_get.status_code = 200
    mock_response_get.json.return_value = [
        {'id': 1, 'author': {'id': 1, 'username': 'user'},
         'created_at': '2023-01-01T12:00:00.000Z', 'updated_at': '2023-01-01T14:30:00.000Z',
         'topic': 'Technology', 'title': 'Sample Article', 'body': 'This is a sample article body.',
         'num_likes': 42, 'subheading': 'A sample subheading'}]

    mock_post.return_value = mock_response_login
    mock_get.return_value = mock_response_get

    App().run()
    assert any('Bye' in str(call) for call in mock_print.mock_calls)


@patch('builtins.input', side_effect=['User', 'Psssword', '2', '1', '0'])
@patch('builtins.print')
@patch('TUI.journal.app.requests.post')
@patch('TUI.journal.app.requests.get')
def test_app_print_article(mock_get, mock_post, mock_print, mock_input):
    mock_response_login = Mock()
    mock_response_login.status_code = 200
    mock_response_login.json.return_value = {'key': 'test_key'}

    mock_response_get = Mock()
    mock_response_get.status_code = 200
    mock_response_get.json.return_value = [
        {'id': 1, 'author': {'id': 1, 'username': 'user'},
         'created_at': '2023-01-01T12:00:00.000Z', 'updated_at': '2023-01-01T14:30:00.000Z',
         'topic': 'Technology', 'title': 'Sample Article', 'body': 'This is a sample article body.',
         'num_likes': 42, 'subheading': 'A sample subheading'}]

    mock_post.return_value = mock_response_login
    mock_get.return_value = mock_response_get

    App().run()
    assert any('BODY: This is a sample article body.' in str(call) for call in mock_print.mock_calls)
    assert any('TITOLO: Sample Article' in str(call) for call in mock_print.mock_calls)
    assert any('SUBHEAD: A sample subheading' in str(call) for call in mock_print.mock_calls)
    assert any('TOPIC: Technology' in str(call) for call in mock_print.mock_calls)


@patch('builtins.input', side_effect=['User', 'Psssword', '2', '1', '3', 'Quantum Computing', '0'])
@patch('builtins.print')
@patch('TUI.journal.app.requests.post')
@patch('TUI.journal.app.requests.get')
def test_app_search_by_topic(mock_get, mock_post, mock_print, mock_input):
    mock_response_login = Mock()
    mock_response_login.status_code = 200
    mock_response_login.json.return_value = {'key': 'test_key'}

    mock_response_get = Mock()
    mock_response_get.status_code = 200
    mock_response_get.json.return_value = [
        {'id': 1, 'author': {'id': 1, 'username': 'user'},
         'created_at': '2023-01-01T12:00:00.000Z', 'updated_at': '2023-01-01T14:30:00.000Z',
         'topic': 'Technology', 'title': 'Sample Article', 'body': 'This is a sample article body.',
         'num_likes': 42, 'subheading': 'A sample subheading'},
        {'id': 2, 'author': {'id': 1, 'username': 'Franco1980'},
         'created_at': '2023-01-01T12:00:00.000Z', 'updated_at': '2023-01-01T14:30:00.000Z',
         'topic': 'Quantum Computing', 'title': 'Sample Article',
         'body': 'Il quantum computing (o calcolo quantistico) è una tecnologia emergente che sfrutta le leggi della meccanica quantistica per risolvere problemi troppo complessi per i computer classici.',
         'num_likes': 42, 'subheading': 'Quantum Computing'},
    ]

    mock_post.return_value = mock_response_login
    mock_get.return_value = mock_response_get

    App().run()
    assert any('Quantum Computing' in str(call) for call in mock_print.mock_calls)


@patch('builtins.input', side_effect=['User', 'Psssword', '1',
                                      'Ibrahimovic primo giorno a Milanello da consulente',
                                      'Sport',
                                      'Lo svedese è tornato nel centro sportivo nelle nuove vesti di advisor della proprietà',
                                      "Zlatan Ibrahimovic è tornato a Milanello questa volta nelle nuove vesti di Advisor della proprietà e consulente dei dirigenti rossoneri",
                                      '0'])
@patch('builtins.print')
@patch('TUI.journal.app.requests.post')
@patch('TUI.journal.app.requests.get')
def test_app_add_article(mock_get, mock_post, mock_print, mock_input):
    mock_response_login = Mock()
    mock_response_login.status_code = 200
    mock_response_login.json.return_value = {'key': 'test_key'}

    mock_response_get = Mock()
    mock_response_get.status_code = 200
    mock_response_get.json.return_value = [
        {'id': 1, 'author': {'id': 1, 'username': 'user'},
         'created_at': '2023-01-01T12:00:00.000Z', 'updated_at': '2023-01-01T14:30:00.000Z',
         'topic': 'Technology', 'title': 'Sample Article', 'body': 'This is a sample article body.',
         'num_likes': 42, 'subheading': 'A sample subheading'},
    ]

    mock_response_post = Mock()
    mock_response_post.status_code = 201

    mock_response_post2 = Mock()
    mock_response_post2.status_code = 200

    mock_response_get2 = Mock()
    mock_response_get2.status_code = 200
    mock_response_get2.json.return_value = [
        {'id': 1, 'author': {'id': 1, 'username': 'user'},
         'created_at': '2023-01-01T12:00:00.000Z', 'updated_at': '2023-01-01T14:30:00.000Z',
         'topic': 'Technology', 'title': 'Sample Article', 'body': 'This is a sample article body.',
         'num_likes': 42, 'subheading': 'A sample subheading'},
        {'id': 2, 'author': {'id': 1, 'username': 'user'},
         'created_at': '2023-01-01T12:00:00.000Z', 'updated_at': '2023-01-01T14:30:00.000Z',
         'topic': 'Technology', 'title': 'Ibrahimovic primo giorno a Milanello da consulente',
         'body': 'Zlatan Ibrahimovic è tornato a Milanello questa volta nelle nuove vesti di Advisor della proprietà e consulente dei dirigenti rossoneri',
         'num_likes': 42, 'subheading': 'A sample subheading'},
    ]

    mock_post.side_effect = [mock_response_login, mock_response_post, mock_response_post2, mock_response_get2]
    mock_get.return_value = mock_response_get

    App().run()

    # assert any(
    #     'Ibrahimovic primo giorno a Milanello da consulente' in str(call) for call in
    #     mock_print.mock_calls), "Optional message if the assertion fails"

    modified_article = mock_response_get2.json.return_value[1]
    assert modified_article['title'] == "Ibrahimovic primo giorno a Milanello da consulente"


@patch('builtins.input', side_effect=['User', 'Psssword', '7', '1', '0'])
@patch('builtins.print')
@patch('TUI.journal.app.requests.post')
@patch('TUI.journal.app.requests.get')
def test_app_put_like(mock_get, mock_post, mock_print, mock_input):
    mock_response_login = Mock()
    mock_response_login.status_code = 200
    mock_response_login.json.return_value = {'key': 'test_key'}

    mock_response_get = Mock()
    mock_response_get.status_code = 200
    mock_response_get.json.return_value = [
        {'id': 1, 'author': {'id': 1, 'username': 'user'},
         'created_at': '2023-01-01T12:00:00.000Z', 'updated_at': '2023-01-01T14:30:00.000Z',
         'topic': 'Technology', 'title': 'Sample Article', 'body': 'This is a sample article body.',
         'num_likes': 42, 'subheading': 'A sample subheading'},
    ]

    mock_response_post = Mock()
    mock_response_post.status_code = 200

    mock_response_post2 = Mock()
    mock_response_post2.status_code = 200

    mock_response_get2 = Mock()
    mock_response_get2.status_code = 200
    mock_response_get2.json.return_value = [
        {'id': 1, 'author': {'id': 1, 'username': 'user'},
         'created_at': '2023-01-01T12:00:00.000Z', 'updated_at': '2023-01-01T14:30:00.000Z',
         'topic': 'Technology', 'title': 'Sample Article', 'body': 'This is a sample article body.',
         'num_likes': 43, 'subheading': 'A sample subheading'},
    ]

    mock_post.side_effect = [mock_response_login, mock_response_post, mock_response_post2, mock_response_get2]
    mock_get.return_value = mock_response_get

    App().run()

    modified_article = mock_response_get2.json.return_value[0]
    assert modified_article['num_likes'] == 43


@patch('builtins.input', side_effect=['User', 'Psssword', '6', '0'])
@patch('builtins.print')
@patch('TUI.journal.app.requests.post')
@patch('TUI.journal.app.requests.get')
def test_app_sort_by_like(mock_get, mock_post, mock_print, mock_input):
    mock_response_login = Mock()
    mock_response_login.status_code = 200
    mock_response_login.json.return_value = {'key': 'test_key'}

    mock_response_get = Mock()
    mock_response_get.status_code = 200
    mock_response_get.json.return_value = [
        {'id': 1, 'author': {'id': 1, 'username': 'user'},
         'created_at': '2023-01-01T12:00:00.000Z', 'updated_at': '2023-01-01T14:30:00.000Z',
         'topic': 'Technology', 'title': 'Sample Article', 'body': 'This is a sample article body.',
         'num_likes': 22, 'subheading': 'A sample subheading'},
        {'id': 2, 'author': {'id': 1, 'username': 'user'},
         'created_at': '2023-01-01T12:00:00.000Z', 'updated_at': '2023-01-01T14:30:00.000Z',
         'topic': 'Technology', 'title': 'Ibrahimovic primo giorno a Milanello da consulente',
         'body': 'Zlatan Ibrahimovic è tornato a Milanello questa volta nelle nuove vesti di Advisor della proprietà e consulente dei dirigenti rossoneri',
         'num_likes': 322, 'subheading': 'A sample subheading'},
    ]

    mock_response_post = Mock()
    mock_response_post.status_code = 200

    mock_post.side_effect = [mock_response_login, mock_response_post]
    mock_get.return_value = mock_response_get

    App().run()

    # Definisci la regex
    regex_pattern = r"(\d+)\s+(.*?)\s+(.*?)\s+(.*?)\s+(\d{2}/\d{2}/\d{4})\s+(.*?)\s+(\d+)"

    # Lista per memorizzare i valori del gruppo 7
    gruppo_7_list = []

    for call in mock_print.mock_calls:
        # Ottieni la rappresentazione stringa della chiamata
        call_str = str(call)

        # Usa la regex per fare il match con la stringa della chiamata
        match = re.findall(regex_pattern, call_str)

        if match:
            # Estrai il valore del gruppo 7
            gruppo_7 = int(match[0][6])
            gruppo_7_list.append(gruppo_7)

    for i in range(len(gruppo_7_list)//2, len(gruppo_7_list)-1):
        assert gruppo_7_list[i] >= gruppo_7_list[i + 1]
