# Job Search Results1

## Описание
Job Search Results1 — это консольное приложение для поиска и анализа вакансий с помощью HeadHunter API,
с возможностью фильтрации, сортировки и сохранения результатов в JSON-файл.

## Структура проекта

~~~
job_search_results1/
│
├── data/
│   └── vacancies.json         # Пример файла с вакансиями (результаты поиска)
│
├── htmlcov/                   # Папка с отчетом покрытия тестов (генерируется автоматически)
│
├── src/
│   ├── __init__.py
│   ├── api_hh.py              # Работа с HeadHunter API
│   ├── config.py              # Конфигурация (USER_AGENT, PATH_TO_JSON)
│   ├── json_saver.py          # Класс для сохранения вакансий в JSON
│   ├── user_interaction.py    # Основной пользовательский интерфейс
│   └── vacancy.py             # Класс Vacancy и работа с вакансиями
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_api_hh.py
│   ├── test_json_saver.py
│   ├── test_user_interaction.py
│   └── test_vacancy.py
│
├── .coverage                  # Файл покрытия тестов
├── .flake8                    # Настройки flake8
├── .gitignore
├── main.py                    # Точка входа (запуск приложения)
├── poetry.lock
├── pyproject.toml
└── README.md                  # Этот файл

~~~

## Как использовать
Для установки и запуска проекта необходимо выполнить следующие шаги:

1.  **Клонируйте репозиторий:**

    ```
    git clone https://github.com/natali83911/job_search_results1.git

    ```

2.  **Перейдите в папку проекта:**

    ```
    cd job_search_results1
    ```

3.  **Установите зависимости с помощью Poetry:**

    ```
    poetry install
    poetry add --group lint flake8
    poetry add --group lint mypy
    poetry add --group lint black
    poetry add --group lint isort
    poetry add --group dev pytest
    poetry add --group dev pytest-cov
    poetry add requests
        
    ```
4.  **Запустите приложение**
    ~~~
    python main.py
    ~~~
    
## Основные возможности
1. Поиск вакансий по ключевым словам, региону и количеству на странице через HeadHunter API.
2. Фильтрация и сортировка вакансий по зарплате и ключевым словам.
3. Сохранение вакансий в файл vacancies.json.
4. Удаление вакансий по URL через пользовательский интерфейс.
5. Тестирование: покрытие кода тестами (pytest).

## Тесты
  Для запуска тестов используйте:
~~~
pytest
~~~
Отчет о покрытии:
~~~
pytest --cov=src --cov-report=html
~~~ 

## Пример использования
~~~
Введите поисковый запрос (ключевое слово): python
Введите количество вакансий на страницу (по умолчанию 20): 10
Введите код региона (по умолчанию 113 — Россия): 113
Введите количество вакансий для вывода в топ N: 5
Введите ключевые слова для фильтрации вакансий (через пробел): django flask
...
Хотите удалить вакансию по URL? (да/нет): да
Введите URL вакансии для удаления: https://hh.ru/vacancy/123456789
Вакансия удалена.
~~~

## Автор
   natali83911
 
