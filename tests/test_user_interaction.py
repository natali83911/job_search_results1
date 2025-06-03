from unittest.mock import patch

from src.api_hh import HeadHunterAPI
from src.json_saver import JSONSaver
from src.user_interaction import user_interaction
from src.vacancy import Vacancy


@patch("builtins.input")
@patch("builtins.print")
@patch.object(HeadHunterAPI, "get_vacancies")
@patch.object(JSONSaver, "add_vacancy")
@patch.object(JSONSaver, "get_vacancies")
@patch.object(JSONSaver, "delete_vacancy")
def test_user_interaction_flow(
    mock_delete_vacancy,
    mock_get_vacancies_file,
    mock_add_vacancy,
    mock_api_get_vacancies,
    mock_print,
    mock_input,
    sample_vacancies_json,
):
    # Настраиваем ввод пользователя по очереди
    # Вводы для get_user_input: keyword, per_page, area
    # Ввод для топ N
    # Ввод для фильтрации по словам
    # Ввод для удаления вакансии (да), URL вакансии
    mock_input.side_effect = [
        "python",  # keyword
        "10",  # per_page
        "113",  # area
        "2",  # топ N
        "django",  # ключевые слова фильтрации
        "да",  # удалить вакансию?
        "http://job1",  # URL для удаления
    ]

    # Возвращаем вакансии из API
    mock_api_get_vacancies.return_value = sample_vacancies_json

    # Возвращаем вакансии из файла (после сохранения)
    mock_get_vacancies_file.return_value = [
        {
            "title": "Python Developer",
            "url": "http://job1",
            "salary": "50000 - 70000 RUR",
            "description": "Python, Django",
        },
        {
            "title": "QA Engineer",
            "url": "http://job2",
            "salary": "Зарплата не указана",
            "description": "Test automation",
        },
    ]

    # Запускаем функцию
    user_interaction()

    # Проверяем, что вакансии получили из API
    mock_api_get_vacancies.assert_called_once_with(keyword="python", per_page=10, area=113)

    # Проверяем, что вакансии добавлялись в JSONSaver
    assert mock_add_vacancy.call_count == len(sample_vacancies_json)

    # Проверяем, что вакансии загружались из файла
    mock_get_vacancies_file.assert_called()

    # Проверяем, что удаление вакансии вызвано с правильным объектом Vacancy
    args, _ = mock_delete_vacancy.call_args
    deleted_vacancy = args[0]
    assert isinstance(deleted_vacancy, Vacancy)
    assert deleted_vacancy.url == "http://job1"

    # Проверяем, что вывод был вызван (print)
    assert mock_print.call_count > 0


@patch("builtins.input")
@patch("builtins.print")
def test_user_interaction_invalid_input(mock_print, mock_input):
    # Проверяем, что при пустом ключевом слове функция завершается
    mock_input.side_effect = ["", ""]

    user_interaction()

    mock_print.assert_any_call("Некорректный ввод параметров. Завершение работы.")
