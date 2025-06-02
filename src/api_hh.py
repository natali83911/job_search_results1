from abc import ABC, abstractmethod

import requests

from .config import USER_AGENT


class AbstractAPI(ABC):
    """Абстрактный базовый класс для API-подключений.
    Определяет интерфейс для подключения и получения вакансий"""

    @abstractmethod
    def _connect(self):
        """Метод подключения к API. Должен быть реализован в наследниках"""
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str, per_page: int):
        """Метод получения вакансий по ключевым словам. Должен быть реализован в наследниках"""
        pass


class HeadHunterAPI(AbstractAPI):
    """Класс для работы с API HeadHunter.
    Реализует методы подключения и получения вакансий"""

    def __init__(self):
        """Инициализация объекта HeadHunterAPI.
        Устанавливает базовый URL и заголовки для запросов"""
        self.__base_url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": USER_AGENT}
        self.__session = None

    def _connect(self):
        """Устанавливает сессию и проверяет доступность API HeadHunter"""
        try:
            self.__session = requests.Session()
            response = self.__session.get(url=self.__base_url, headers=self.__headers)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            raise ConnectionError(f"Ошибка подключения к API: {e}")

    def get_vacancies(self, keyword: str, per_page: int = 20, area: int = 113):
        """Получает список вакансий по ключевому слову с параметрами пагинации и региона"""
        self._connect()
        params = {"text": keyword, "per_page": per_page, "area": area}
        response = requests.get(url=self.__base_url, params=params, headers=self.__headers)
        if response.status_code != 200:
            raise ConnectionError(f"Ошибка получения вакансий: {response.status_code}")
        data = response.json()
        return data.get("items", [])
