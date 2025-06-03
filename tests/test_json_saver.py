from src.json_saver import JSONSaver
from src.vacancy import Vacancy


def test_add_and_get_vacancy(json_saver, sample_vacancy):
    assert json_saver.get_vacancies() == []
    json_saver.add_vacancy(sample_vacancy)
    vacancies = json_saver.get_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0]["title"] == sample_vacancy.title
    assert vacancies[0]["url"] == sample_vacancy.url


def test_add_duplicate_vacancy(json_saver, sample_vacancy):
    json_saver.add_vacancy(sample_vacancy)
    json_saver.add_vacancy(sample_vacancy)
    vacancies = json_saver.get_vacancies()
    assert len(vacancies) == 1


def test_get_vacancies_with_filter(json_saver, sample_vacancy):
    json_saver.add_vacancy(sample_vacancy)
    json_saver.add_vacancy(Vacancy("Another Job", "http://another.com", "60000", "Another description"))

    filtered = json_saver.get_vacancies(criteria={"title": "test"})
    assert len(filtered) == 1
    assert filtered[0]["title"] == sample_vacancy.title

    filtered = json_saver.get_vacancies(criteria={"description": "another"})
    assert len(filtered) == 1
    assert filtered[0]["title"] == "Another Job"


def test_delete_vacancy(json_saver, sample_vacancy):
    json_saver.add_vacancy(sample_vacancy)
    json_saver.add_vacancy(Vacancy("Job 2", "http://job2.com", "40000", "Desc 2"))

    json_saver.delete_vacancy(sample_vacancy)
    vacancies = json_saver.get_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0]["url"] != sample_vacancy.url


def test_get_vacancies_file_not_exist(tmp_path):
    file_path = tmp_path / "nonexistent.json"
    saver = JSONSaver(str(file_path))
    assert saver.get_vacancies() == []


def test_get_vacancies_corrupted_file(tmp_path):
    file_path = tmp_path / "corrupted.json"
    file_path.write_text("not a json")
    saver = JSONSaver(str(file_path))
    assert saver.get_vacancies() == []
