"""Модуль реализации функции через pytest.addoption"""
import requests


def test_req_addopt(pytestconfig):
    """
    Проверка, что при get-запросе url, введенного через командную строку в параметре --url,
    возвращается код, идентичный коду, введенному через командную строку в параметре --status_code
    """
    url = pytestconfig.getoption("--url")
    status_code = int(pytestconfig.getoption("--status_code"))

    assert requests.get(url).status_code == status_code, ('Возвращенный статус код не соответствует заданному в '
                                                          'параметре --status_code')
