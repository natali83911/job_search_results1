import json
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any

from .config import PATH_TO_JSON
from .vacancy import Vacancy



class AbstractSaver(ABC):
    """Абстрактный класс для сохранения вакансий.
    Определяет интерфейс для добавления, получения и удаления вакансий."""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансию в хранилище"""
        pass

    @abstractmethod
    def get_vacancies(self, criteria: Optional[Dict[str, str]] = None) -> List[Dict[str, Any]]:
        """Получает список вакансий из хранилища"""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансию из хранилища, если такая вакансия уже имеется"""
        pass


class JSONSaver(AbstractSaver):
    """Класс для сохранения вакансий в JSON-файл"""

    def __init__(self, filename=PATH_TO_JSON):
        """Инициализация экземпляра JSONSaver"""
        self.__filename = filename

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансию в JSON-файл, если вакансии с таким URL ещё нет"""
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

    def get_vacancies(self, criteria: Optional[Dict[str, str]] = None) -> List[Dict[str, Any]]:
        """Загружает вакансии из JSON-файла и при необходимости фильтрует их по критериям"""
        try:
            with open(self.__filename, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    # Если файл пустой или повреждённый, считаем, что данных нет
                    data = []
        except FileNotFoundError:
            data = []

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

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаляет вакансию из JSON-файла по совпадению URL"""
        data = self.get_vacancies() or []
        data = [v for v in data if v["url"] != vacancy.url]
        with open(self.__filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
