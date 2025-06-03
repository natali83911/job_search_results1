import re
from typing import Any, Dict, List, Optional


class Vacancy:
    """Класс, представляющий вакансию с основными атрибутами:
    - title: название вакансии
    - url: ссылка на вакансию
    - salary: информация о зарплате (строка)
    - description: описание вакансии"""

    __slots__ = ["title", "url", "salary", "description"]

    def __init__(self, title: str, url: str, salary: str, description: str):
        """Инициализация объекта вакансии.

        :param title: название вакансии
        :param url: ссылка на вакансию
        :param salary: зарплата в виде строки
        :param description: описание вакансии"""
        self.title = title
        self.url = url
        self.salary = self._validate_salary(salary)
        self.description = description

    def _validate_salary(self, salary: Optional[str]) -> str:
        """Проверяет и нормализует значение зарплаты"""
        if not salary or salary == "" or salary is None:
            return "Зарплата не указана"
        return salary

    # Методы сравнения по зарплате
    def __lt__(self, other: "Vacancy") -> bool:
        return self._salary_to_int() < other._salary_to_int()

    def __le__(self, other: "Vacancy") -> bool:
        return self._salary_to_int() <= other._salary_to_int()

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self._salary_to_int() == other._salary_to_int()

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self._salary_to_int() != other._salary_to_int()

    def __gt__(self, other: "Vacancy") -> bool:
        return self._salary_to_int() > other._salary_to_int()

    def __ge__(self, other: "Vacancy") -> bool:
        return self._salary_to_int() >= other._salary_to_int()

    def _salary_to_int(self) -> int:
        """Преобразует строку зарплаты в целое число для сравнения.
        Берёт первое найденное число в строке.
        Если чисел нет — возвращает 0"""
        if isinstance(self.salary, str):
            nums = re.findall(r"\d+", self.salary.replace(" ", ""))
            if nums:
                return int(nums[0])
            else:
                return 0
        elif isinstance(self.salary, (int, float)):
            return int(self.salary)
        else:
            return 0

    @classmethod
    def cast_to_object_list(cls, vacancies_json: List[Dict[str, Any]]) -> List["Vacancy"]:
        """Преобразует список вакансий в формате JSON (список словарей) в список объектов Vacancy"""
        objects = []
        for item in vacancies_json:
            title = item.get("name", "Без названия")
            url = item.get("alternate_url", "")
            salary_info = item.get("salary")
            if salary_info:
                salary = ""
                if salary_info.get("from") and salary_info.get("to"):
                    salary = f"{salary_info['from']} - {salary_info['to']} {salary_info.get('currency', '')}"
                elif salary_info.get("from"):
                    salary = f"от {salary_info['from']} {salary_info.get('currency', '')}"
                elif salary_info.get("to"):
                    salary = f"до {salary_info['to']} {salary_info.get('currency', '')}"
                else:
                    salary = "Зарплата не указана"
            else:
                salary = "Зарплата не указана"
            description = (
                item.get("snippet", {}).get("requirement", "")
                or item.get("snippet", {}).get("responsibility", "")
                or ""
            )
            vacancy = cls(title, url, salary, description)
            objects.append(vacancy)
        return objects
