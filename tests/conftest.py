import pytest

from src.api_hh import HeadHunterAPI
from src.json_saver import JSONSaver
from src.vacancy import Vacancy


@pytest.fixture
def api():
    return HeadHunterAPI()


@pytest.fixture
def vacancy():
    return Vacancy("Test", "http://url", "50000", "desc")


@pytest.fixture
def sample_vacancy():
    return Vacancy(title="Test Job", url="http://testjob.com", salary="50000", description="Test description")


@pytest.fixture
def json_saver(tmp_path):
    file_path = tmp_path / "vacancies.json"
    return JSONSaver(str(file_path))


@pytest.fixture
def sample_vacancies_json():
    return [
        {
            "name": "Python Developer",
            "alternate_url": "http://job1",
            "salary": {"from": 50000, "to": 70000, "currency": "RUR"},
            "snippet": {"requirement": "Python, Django"},
        },
        {
            "name": "QA Engineer",
            "alternate_url": "http://job2",
            "salary": None,
            "snippet": {"responsibility": "Test automation"},
        },
    ]
