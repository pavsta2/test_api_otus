"""Модуль проверок DOG API"""
import requests
import pytest

LIST_ALL_BREEDS = 'https://dog.ceo/api/breeds/list/all'


def send_request_no_params(url):
    """Функция отправки get запроса без параметров"""
    return requests.get(url)


def send_request_all_breed_imgs(breed):
    """
    Функция отправки запроса всех фото породы
    """
    return requests.get(f'https://dog.ceo/api/breed/{breed}/images')


def send_request_rand_breed_imgs(breed):
    """
    Функция отправки запроса одной рандомной фото породы
    """
    return requests.get(f'https://dog.ceo/api/breed/{breed}/images/random')


def send_request_num_of_breed_imgs(breed, random):
    """
    Функция отправки запроса заданного кол-ва рандомных фото породы
    """
    return requests.get(f'https://dog.ceo/api/breed/{breed}/images/random/{random}')


def send_request_all_sub_breed_imgs(breed, sub_breed):
    """
        Функция отправки запроса на все фото под-породы
    """
    return requests.get(f'https://dog.ceo/api/breed/{breed}/{sub_breed}/images')


def send_request_num_of_sub_breed_imgs(breed, sub_breed, random):
    """
        Функция отправки запроса заданного кол-ва рандомных фото под-породы
    """

    return requests.get(f'https://dog.ceo/api/breed/{breed}/{sub_breed}/images/{random}')


def send_request_rand_sub_breed_imgs(breed, sub_breed):
    """
        Функция отправки запроса заданного кол-ва рандомных фото под-породы
    """
    return requests.get(f'https://dog.ceo/api/breed/{breed}/{sub_breed}/images/random')


def test_list_all_breeds():
    """Позитивная проверка получения списка всех пород"""
    assert send_request_no_params(LIST_ALL_BREEDS).status_code == 200, 'Возвращается код, отличный от 200'
    assert send_request_no_params(LIST_ALL_BREEDS).json()['status'] == 'success', ('В поле "status" JSON содержится'
                                                                                   'значение, отличное от "success"')


@pytest.mark.parametrize('breeds',
                         ['bulldog',
                          'greyhound',
                          'hound'],
                         ids=[
                             'bulldog',
                             'greyhound',
                             'hound'
                         ])
def test_get_single_breed_img_posit(breeds):
    """Позитивные проверки получение одной рандомной фото породы"""
    assert send_request_rand_breed_imgs(breeds).status_code == 200, 'Возвращается код, отличный от 200'
    # проверяем, что в message возвращается строка с один url, а не массив:
    assert isinstance((send_request_rand_breed_imgs(breeds).json()['message']),
                      str), 'В ответе не одно фото'
    # проверяем, что в url есть название запрошенной породы
    assert send_request_rand_breed_imgs(breeds).json()['message'].find(breeds) != -1, ('В url фото нет '
                                                                                       'упоминания '
                                                                                       'запрошенной '
                                                                                       'породы')


@pytest.mark.parametrize('breeds',
                         ['bulldog',
                          'greyhound',
                          'hound'],
                         ids=[
                             'bulldog',
                             'greyhound',
                             'hound'
                         ])
def test_get_all_breed_images_posit(breeds):
    """Позитивные проверки получения всех фото породы"""
    assert send_request_all_breed_imgs(breeds).status_code == 200, 'Возвращается код, отличный от 200'
    # проверяем, что в url есть название запрошенной породы
    for i in send_request_all_breed_imgs(breeds).json()['message']:
        assert i.find(breeds) != -1, 'В url фото нет упоминания запрошенной породы'


@pytest.mark.parametrize('breeds',
                         ['big_dog'],
                         ids=['wrong_breed'])
def test_get_all_breed_images_negot(breeds):
    """Негативные проверки получения всех фото породы"""
    assert send_request_all_breed_imgs(breeds).status_code == 404, 'Возвращается код, отличный от 404'


@pytest.mark.parametrize('breeds',
                         [('hound', 'afghan'),
                          ('mastiff', 'bull'),
                          ('sheepdog', 'english')],
                         ids=[
                             'hound-afghan',
                             'mastiff-bull',
                             'sheepdog-english'
                         ])
def test_get_all_sub_breed_images_posit(breeds):
    """Позитивные проверки получения всех фото под-породы"""
    assert send_request_all_sub_breed_imgs(breeds[0], breeds[1]).status_code == 200, 'Возвращается код, отличный от 200'
    respons_img = send_request_all_sub_breed_imgs(breeds[0], breeds[1]).json()['message']
    # проверяем, что в url есть название запрошенной породы и под-породы
    for i in respons_img:
        assert i.find(f'{breeds[0]}-{breeds[1]}') != -1, ('В url фото нет упоминания запрошенной породы '
                                                          'и под-породы')


@pytest.mark.parametrize('num',
                         [3, 10, 100],
                         ids=['2', '10', '100'])
def test_breed_multi_random_images_posit(num):
    """Позитивные проверки получения определенного кол-во рандомных фото породы"""
    assert send_request_num_of_breed_imgs('bulldog', random=num).status_code == 200, 'Возвращается код, отличный от 200'
    # проверяем, что кол-во записей в возвращенном массиве адресов равно запрошенному кол-ву num
    assert len(send_request_num_of_breed_imgs('bulldog', random=num).json()['message']) == num, (f'Возвращается кол-во '
                                                                                                 f'url фото, отличное '
                                                                                                 f'от {num}')
