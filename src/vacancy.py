import re

from src.api_hh import HeadHunterAPI


class Vacancy:
    __slots__ = ["title", "url", "salary", "description"]

    def __init__(self, title: str, url: str, salary: str, description: str):
        self.title = title
        self.url = url
        self.salary = self._validate_salary(salary)
        self.description = description

    def _validate_salary(self, salary):
        if not salary or salary == "" or salary is None:
            return "Зарплата не указана"
        return salary

    # Методы сравнения по зарплате
    def __lt__(self, other):
        return self._salary_to_int() < other._salary_to_int()

    def __le__(self, other):
        return self._salary_to_int() <= other._salary_to_int()

    def __eq__(self, other):
        return self._salary_to_int() == other._salary_to_int()

    def __ne__(self, other):
        return self._salary_to_int() != other._salary_to_int()

    def __gt__(self, other):
        return self._salary_to_int() > other._salary_to_int()

    def __ge__(self, other):
        return self._salary_to_int() >= other._salary_to_int()

    def _salary_to_int(self):
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
    def cast_to_object_list(cls, vacancies_json):
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
