"""Модуль проверок Brewery API"""
import json
import random
import string
from typing import Optional
import requests
import pytest
from pydantic import BaseModel


class Brewery(BaseModel):
    """Класс для описания json-модели пивоваренного завода"""
    id: str
    name: str
    brewery_type: str
    address_1: Optional[str] = None
    address_2: Optional[str] = None
    address_3: Optional[str] = None
    city: Optional[str] = None
    state_province: Optional[str] = None
    postal_code: Optional[str] = None
    country: Optional[str] = None
    longitude: Optional[str] = None
    latitude: Optional[str] = None
    phone: Optional[str] = None
    website_url: Optional[str] = None
    state: Optional[str] = None
    street: Optional[str] = None


def get_random_brewery_id():
    """Функция для получения рандомного id пивоварни"""
    url = 'https://api.openbrewerydb.org/v1/breweries/random'
    response = requests.get(url)
    random_id = response.json()[0]['id']
    return random_id


def get_brewery_by_id(br_id: str):
    """Функция для получения записи о пивоварне пo id"""
    url = f'https://api.openbrewerydb.org/v1/breweries/{br_id}'
    return requests.get(url)


def get_brewery_by_type(br_type: str):
    """Функция для получения списка пивоварен пo типу"""
    url = f'https://api.openbrewerydb.org/v1/breweries?by_type={br_type}'
    return requests.get(url)


def get_n_breweries_on_page(num: str):
    """Функция для получения списка пивоварен с кол-вом n на странице"""
    url = f'https://api.openbrewerydb.org/v1/breweries?per_page={num}'
    return requests.get(url)


@pytest.mark.parametrize('br_id',
                         [get_random_brewery_id()],
                         ids=['random valid id'])
def test_get_brewery_by_id_posit(br_id):
    """Позитивные проверки получения пивоварни по id
    + проверка модели пивоварни"""
    response = get_brewery_by_id(br_id)
    assert response.status_code == 200, f'Возвращается код, отличный от 200: {response.status_code}'

    Brewery.model_validate_json(response.text)


@pytest.mark.parametrize('br_id',
                         [f'{random.choices(string.ascii_letters + string.digits, k=8)}-'
                          f'{random.choices(string.ascii_letters + string.digits, k=4)}-'
                          f'{random.choices(string.ascii_letters + string.digits, k=4)}-'
                          f'{random.choices(string.ascii_letters + string.digits, k=4)}-'
                          f'{random.choices(string.ascii_letters + string.digits, k=12)}'],
                         ids=['random invalid id'])
def test_get_brewery_by_id_negot(br_id):
    """Негативные проверки получения пивоварни по рандомному не валидному id,
    составленному в формате валидного"""
    response = get_brewery_by_id(br_id)
    assert response.status_code == 404, f'Возвращается код, отличный от 404: {response.status_code}'


@pytest.mark.parametrize('br_type',
                         ['micro',
                          'nano',
                          'regional',
                          'brewpub',
                          'large',
                          'planning',
                          'bar',
                          'contract',
                          'proprietor',
                          'closed'],
                         ids=['micro',
                              'nano',
                              'regional',
                              'brewpub',
                              'large',
                              'planning',
                              'bar',
                              'contract',
                              'proprietor',
                              'closed'])
def test_get_brewery_by_type_posit(br_type):
    """Позитивные проверки получения пивоварни по типу
    + проверка модели пивоварни"""
    response = get_brewery_by_type(br_type)
    assert response.status_code == 200, f'Возвращается код, отличный от 200: {response.status_code}'

    Brewery.model_validate_json(json.dumps(response.json()[0]))
    for brew in response.json():
        assert brew['brewery_type'] == br_type, (f'Тип пивоварни не соответствует заданному, '
                                                 f'exp: {br_type}, fact: {brew["brewery_type"]}')


@pytest.mark.parametrize('br_type',
                         ['invalid_type_name'],
                         ids=['invalid_type_name'])
def test_get_brewery_by_type_negot(br_type):
    """Негативные проверки получения пивоварни по типу"""
    response = get_brewery_by_type(br_type)
    assert response.status_code == 400, f'Возвращается код, отличный от 400: {response.status_code}'


@pytest.mark.parametrize('num',
                         ['50', '100', '200'],
                         ids=['n=50', 'n=100', 'n=200'])
def test_get_num_of_brew_per_page_posit(num):
    """Позитивные проверки получения списка пивоварен с заданным кол-во на странице"""
    response = get_n_breweries_on_page(num)
    assert response.status_code == 200, f'Возвращается код, отличный от 200: {response.status_code}'

    assert len(response.json()) == int(num), (f'Кол-во пивоварен на странице не равно заданному кол-ву. '
                                              f'exp: {num}, fact: {len(response.json())}')


@pytest.mark.parametrize('num',
                         [''],
                         ids=['no param (default)'])
def test_get_default_num_of_brew_per_page_posit(num):
    """Позитивные проверки получения списка пивоварен с дефолтным кол-во на странице"""
    response = get_n_breweries_on_page(num)
    assert response.status_code == 200, f'Возвращается код, отличный от 200: {response.status_code}'

    assert len(response.json()) == 50, (f'Кол-во пивоварен на странице не равно дефолтному. '
                                        f'exp: 50, fact: {len(response.json())}')


@pytest.mark.parametrize('num',
                         ['201', '500'],
                         ids=['n=201', 'n=500'])
def test_get_num_of_brew_per_page_negot(num):
    """Негативные проверки получения списка пивоварен с заданным невалидным (более 200) кол-вом на странице"""
    response = get_n_breweries_on_page(num)
    assert response.status_code == 200, f'Возвращается код, отличный от 200: {response.status_code}'

    assert len(response.json()) == 200, (f'Кол-во пивоварен на странице не равно максимальному кол-ву. '
                                         f'exp: 200, fact: {len(response.json())}')
