from src.vacancy import Vacancy


def test_validate_salary():
    v1 = Vacancy("Test", "http://url", "", "desc")
    assert v1.salary == "Зарплата не указана"

    v2 = Vacancy("Test", "http://url", None, "desc")
    assert v2.salary == "Зарплата не указана"

    v3 = Vacancy("Test", "http://url", "50000", "desc")
    assert v3.salary == "50000"


def test_salary_to_int(vacancy):
    vacancy.salary = "от 50 000 руб."
    assert vacancy._salary_to_int() == 50000

    vacancy.salary = "до 100000"
    assert vacancy._salary_to_int() == 100000

    vacancy.salary = "нет данных"
    assert vacancy._salary_to_int() == 0

    vacancy.salary = 75000
    assert vacancy._salary_to_int() == 75000


def test_comparisons():
    v1 = Vacancy("Job1", "url1", "50000", "desc")
    v2 = Vacancy("Job2", "url2", "70000", "desc")

    assert v1 < v2
    assert v1 <= v2
    assert v2 > v1
    assert v2 >= v1
    assert v1 != v2

    v3 = Vacancy("Job3", "url3", "50000", "desc")
    assert v1 == v3


def test_cast_to_object_list():
    json_data = [
        {
            "name": "Developer",
            "alternate_url": "http://job1",
            "salary": {"from": 50000, "to": 70000, "currency": "RUR"},
            "snippet": {"requirement": "Python, Django"},
        },
        {
            "name": "Tester",
            "alternate_url": "http://job2",
            "salary": None,
            "snippet": {"responsibility": "Test automation"},
        },
        {"name": "Manager", "alternate_url": "http://job3", "salary": {"from": 60000}, "snippet": {}},
    ]

    vacancies = Vacancy.cast_to_object_list(json_data)
    assert len(vacancies) == 3
    assert vacancies[0].title == "Developer"
    assert vacancies[0].salary == "50000 - 70000 RUR"
    assert "Python" in vacancies[0].description

    assert vacancies[1].salary == "Зарплата не указана"
    assert "Test automation" in vacancies[1].description

    assert vacancies[2].salary == "от 60000 "
    assert vacancies[2].description == ""
