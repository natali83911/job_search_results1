import json
from abc import ABC, abstractmethod

from src.api_hh import HeadHunterAPI
from src.config import PATH_TO_JSON
from src.vacancy import Vacancy


class AbstractSaver(ABC):

    @abstractmethod
    def add_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies(self, criteria=None):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        pass


class JSONSaver(AbstractSaver):
    def __init__(self, filename=PATH_TO_JSON):
        self.__filename = filename

    def add_vacancy(self, vacancy):
        data = self.get_vacancies() or []
        if not any(v["url"] == vacancy.url for v in data):
            data.append(
                {
                    "title": vacancy.title,
                    "url": vacancy.url,
                    "salary": vacancy.salary,
                    "description": vacancy.description,
                }
            )
            with open(self.__filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

    def get_vacancies(self, criteria=None):
        try:
            with open(self.__filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            return []
        if criteria is None:
            return data
        filtered = []
        for v in data:
            match = True
            for key, value in criteria.items():
                if key not in v or value.lower() not in str(v[key]).lower():
                    match = False
                    break
            if match:
                filtered.append(v)
        return filtered

    def delete_vacancy(self, vacancy):
        data = self.get_vacancies() or []
        data = [v for v in data if v["url"] != vacancy.url]
        with open(self.__filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    api = HeadHunterAPI()
    vacancies_json = api.get_vacancies(keyword="Python", per_page=5, area=113)  # 113 — Россия
    print(f"Найдено вакансий: {len(vacancies_json)}")

    vacancies = Vacancy.cast_to_object_list(vacancies_json)

    for vac in vacancies:
        print(f"Название: {vac.title}")
        print(f"Ссылка: {vac.url}")
        print(f"Зарплата: {vac.salary}")
        print(f"Описание: {vac.description[:100]}...")
        print("-" * 40)

    saver = JSONSaver()
    for vac in vacancies:
        saver.add_vacancy(vac)

    # for vac in vacancies:
    #     saver.delete_vacancy(vac)
