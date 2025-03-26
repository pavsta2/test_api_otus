"""Модуль проверок JSON Placeholder API"""
import json
from typing import Optional
import requests
import pytest
from pydantic import BaseModel



class Post(BaseModel):
    """Класс для описания json-модели поста"""
    id: Optional[int] = None
    userId: int
    title: str
    body: str


def get_posts(post_id=None):
    """Функция для get-запроса постов (всех или заданного кол-ва)"""
    if post_id is None:
        response = requests.get('https://jsonplaceholder.typicode.com/posts',
                                timeout=100)
        return response
    response = requests.get(f'https://jsonplaceholder.typicode.com/posts/{post_id}',
                            timeout=100)
    return response


def create_post(body: str):
    """Функция для post-запроса создания поста"""
    headers = {'Content-type': 'application/json; charset=UTF-8'}
    response = requests.post(data=body,
                             headers=headers,
                             url='https://jsonplaceholder.typicode.com/posts',
                             timeout=100)
    return response


def update_post(body: str, post_id: int):
    """Функция для put-запроса изменения всего поста"""
    headers = {'Content-type': 'application/json; charset=UTF-8'}
    response = requests.put(data=body,
                            headers=headers,
                            url=f'https://jsonplaceholder.typicode.com/posts/{post_id}',
                            timeout=100)
    return response


def test_get_all_posts():
    """Позитивная проверка эндпоинта получения всех постов + модели записи поста"""
    response = get_posts()
    assert response.status_code == 200, f'Возвращается код, отличный от 200: {response.status_code}'

    one_post_json = json.dumps(response.json()[0])
    Post.model_validate_json(one_post_json)


@pytest.mark.parametrize('post_id',
                         [1, 20, 100],
                         ids=['id=1', 'id=20', 'id=100'])
def test_get_one_post_posit(post_id):
    """Позитивные проверки эндпоинта получения одного поста + модели записи поста"""
    response = get_posts(post_id=post_id)
    assert response.status_code == 200, f'Возвращается код, отличный от 200: {response.status_code}'

    post_json = response.text
    Post.model_validate_json(post_json)
    post = Post(**response.json())
    assert post.id == post_id, f'id ожидаемый: {post_id}, а полученный: {post.id}'


@pytest.mark.parametrize('post_id',
                         [101, 200],
                         ids=['101-not exist id', '200-not exist id'])
def test_get_one_post_negot(post_id):
    """Негативные проверки эндпоинта получения одного поста + модели записи поста"""
    response = get_posts(post_id=post_id)
    assert response.status_code == 404, f'Возвращается код, отличный от 404: {response.status_code}'


@pytest.mark.parametrize('title, body, user_id',
                         [('some title', 'some body', 1)],
                         ids=['valid title, valid body and valid userId'])
def test_create_post_posit(title, body, user_id):
    """Позитивные проверки эндпоинта создания поста"""
    post = Post(title=title, body=body, userId=user_id)
    response = create_post(post.model_dump_json())

    assert response.status_code == 201, f'Возвращается код, отличный от 201: {response.status_code}'
    assert response.json()['userId'] == post.userId
    assert response.json()['title'] == post.title
    assert response.json()['body'] == post.body


@pytest.mark.parametrize('title, body, userId, post_id',
                         [('some title', 'some body', 1, 5)],
                         ids=['valid title, valid body, valid userId, valid id'])
def test_post_update_posit(title, body, userId, post_id):
    """Позитивные проверки эндпоинта изменения поста"""
    post = Post(title=title, body=body, userId=userId)
    response = update_post(post.model_dump_json(), post_id)

    assert response.status_code == 200, f'Возвращается код, отличный от 200: {response.status_code}'
    assert response.json()['userId'] == post.userId
    assert response.json()['title'] == post.title
    assert response.json()['body'] == post.body
    assert response.json()['id'] == post_id
