"""Модуль проверок DOG API"""
import requests
import pytest

LIST_ALL_BREEDS = 'https://dog.ceo/api/breeds/list/all'


def send_request_no_params(url):
    """Функция отправки get запроса без параметров"""
    return requests.get(url)


def send_request_breed_imgs(breed, random=None):
    """
    Функция отправки запроса на:
    - все фото породы
    - одной рандомной фото породы
    - заданного кол-ва рандомных фото породы
    """
    if isinstance(random, int):
        return requests.get(f'https://dog.ceo/api/breed/{breed}/images/random/{random}')
    elif random == 'random':
        return requests.get(f'https://dog.ceo/api/breed/{breed}/images/random')
    else:
        return requests.get(f'https://dog.ceo/api/breed/{breed}/images')


def send_request_sub_breed_imgs(breed, sub_breed, random=None):
    """
        Функция отправки запроса на:
        - все фото под-породы
        - одной рандомной фото под-породы
        - заданного кол-ва рандомных фото под-породы
        """
    if isinstance(random, int):
        return requests.get(f'https://dog.ceo/api/breed/{breed}/{sub_breed}/images/{random}')
    elif random == 'random':
        return requests.get(f'https://dog.ceo/api/breed/{breed}/{sub_breed}/images/random')
    else:
        return requests.get(f'https://dog.ceo/api/breed/{breed}/{sub_breed}/images')


def test_list_all_breeds():
    """Позитивная проверка получения списка всех пород"""
    assert send_request_no_params(LIST_ALL_BREEDS).status_code == 200, 'Возвращается код, отличный от 200'
    assert send_request_no_params(LIST_ALL_BREEDS).json()['status'] == 'success', ('В поле "status" JSON содержится'
                                                                                   'значение, отличное от "success"')


@pytest.mark.parametrize('breeds',
                         ['bulldog',
                          'greyhound',
                          'hound'],
                         ids = [
                          'bulldog',
                          'greyhound',
                          'hound'
                         ])
def test_get_single_breed_img_posit(breeds):
    """Позитивные проверки получение одной рандомной фото породы"""
    assert send_request_breed_imgs(breeds, random='random').status_code == 200, 'Возвращается код, отличный от 200'
    # проверяем, что в message возвращается строка с один url, а не массив:
    assert isinstance((send_request_breed_imgs(breeds, random='random').json()['message']), str), 'В ответе не одно фото'
    # проверяем, что в url есть название запрошенной породы
    assert send_request_breed_imgs(breeds, random='random').json()['message'].find(breeds) != -1, ('В url фото нет '
                                                                                                      'упоминания '
                                                                                                      'запрошенной '
                                                                                                      'породы')


@pytest.mark.parametrize('breeds',
                         ['bulldog',
                          'greyhound',
                          'hound'],
                         ids = [
                          'bulldog',
                          'greyhound',
                          'hound'
                         ])
def test_get_all_breed_images_posit(breeds):
    """Позитивные проверки получения всех фото породы"""
    assert send_request_breed_imgs(breeds).status_code == 200, 'Возвращается код, отличный от 200'
    # проверяем, что в url есть название запрошенной породы
    assert send_request_breed_imgs(breeds).json()['message'][0].find(breeds) != -1, ('В url фото нет упоминания '
                                                                                     'запрошенной породы')


@pytest.mark.parametrize('breeds',
                         ['big_dog'],
                         ids = ['wrong_breed'])
def test_get_all_breed_images_negot(breeds):
    """Негативные проверки получения всех фото породы"""
    assert send_request_breed_imgs(breeds).status_code == 404, 'Возвращается код, отличный от 404'


@pytest.mark.parametrize('breeds',
                         [('hound', 'afghan'),
                          ('mastiff', 'bull'),
                          ('sheepdog', 'english')],
                         ids = [
                          'hound-afghan',
                          'mastiff-bull',
                          'sheepdog-english'
                         ])
def test_get_all_sub_breed_images_posit(breeds):
    """Позитивные проверки получения всех фото под-породы"""
    assert send_request_sub_breed_imgs(breeds[0], breeds[1]).status_code == 200, 'Возвращается код, отличный от 200'
    respons_img = send_request_breed_imgs(breeds[0], breeds[1]).json()['message'][0]
    # проверяем, что в url есть название запрошенной породы и под-породы
    assert respons_img.find(f'{breeds[0]}-{breeds[1]}') != -1, ('В url фото нет упоминания запрошенной породы '
                                                                'и под-породы')


@pytest.mark.parametrize('num',
                         [3, 10, 100],
                         ids = ['2', '10', '100'])
def test_breed_multi_random_images_posit(num):
    """Позитивные проверки получения определенного кол-во рандомных фото породы"""
    assert send_request_breed_imgs('bulldog', random=num).status_code == 200, 'Возвращается код, отличный от 200'
    # проверяем, что кол-во записей в возвращенном массиве адресов равно запрошенному кол-ву num
    assert len(send_request_breed_imgs('bulldog', random=num).json()['message']) == num, (f'Возвращается кол-во '
                                                                                          f'url фото, отличное '
                                                                                          f'от {num}')
