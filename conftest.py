"""Модуль фикстур"""


def pytest_addoption(parser):
    """Pytest hook для добавления кастомных параметров командной строки"""
    parser.addoption("--url", action="store", default="https://ya.ru", help="url")
    parser.addoption("--status_code", action="store", default=200, help="status_code")