from abc import ABC, abstractmethod

import requests

from config import USER_AGENT


class AbstractAPI(ABC):

    @abstractmethod
    def _connect(self):
        """Метод подключения к API"""
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str, per_page: int):
        """Метод получения вакансий по ключам"""
        pass


class HeadHunterAPI(AbstractAPI):

    def __init__(self):
        self.__base_url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": USER_AGENT}
        self.__session = None

    def _connect(self):
        """Метод подключения к API"""
        try:
            self.__session = requests.Session()
            response = self.__session.get(url=self.__base_url, headers=self.__headers)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            raise ConnectionError(f"Ошибка подключения к API: {e}")

    def get_vacancies(self, keyword: str, per_page: int, area: int):
        """Метод получения вакансий по ключам"""
        self._connect()
        params = {"text": keyword, "per_page": per_page, "area": area}
        response = requests.get(url=self.__base_url, params=params, headers=self.__headers)
        if response.status_code != 200:
            raise ConnectionError(f"Ошибка получения вакансий: {response.status_code}")
        data = response.json()
        return data.get("items", [])


# if __name__ == "__main__":
#
#     api = HeadHunterAPI()
#     vacancies = api.get_vacancies(keyword="Python", per_page=5, area=113)  # 113 — Россия
#     print(f"Найдено вакансий: {len(vacancies)}")
#     for v in vacancies:
#         print(f"{v['name']} | {v.get('salary')} | {v['alternate_url']}")
