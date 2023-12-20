import dataclasses
from dataclasses import InitVar
from pathlib import Path
from typing import Any
from unittest import mock
from unittest.mock import MagicMock, patch, mock_open, Mock, call

from TUI.journal.app import App, main
from TUI.journal.domain import Article


@patch('builtins.input', side_effect=['0'])
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


@patch('builtins.input', side_effect=['2', '1', '0'])
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


@patch('builtins.input', side_effect=['2', '1', '3', 'Quantum Computing', '0'])
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


@patch('builtins.input', side_effect=['1',
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

    mock_post.side_effect = [mock_response_login, mock_response_post, mock_response_post2]
    mock_get.return_value = mock_response_get

    App().run()

    # Your specific assert statement based on the expected behavior
    # Modify this according to what you are testing
    assert any(
        'Ibrahimovic primo giorno a Milanello da consulente' in str(call) for call in
        mock_print.mock_calls), "Optional message if the assertion fails"
