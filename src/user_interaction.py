from .api_hh import HeadHunterAPI
from .config import PATH_TO_JSON
from .json_saver import JSONSaver
from .vacancy import Vacancy
from typing import Optional, Tuple, List



def get_user_input() -> Optional[Tuple[str, int, int]]:
    """Запрашивает у пользователя параметры поиска вакансий:
    ключевое слово, количество вакансий на страницу и регион"""

    keyword: str = input("Введите поисковый запрос (ключевое слово): ").lower().strip()
    if not keyword:
        print("Поисковый запрос не может быть пустым.")
        return None

    while True:
        per_page_str: str = input("Введите количество вакансий на страницу (по умолчанию 20): ").strip()
        if not per_page_str:
            per_page: int = 20
            break
        if per_page_str.isdigit() and int(per_page_str) > 0:
            per_page = int(per_page_str)
            break
        else:
            print("Пожалуйста, введите положительное целое число.")

    while True:
        area_str: str = input("Введите код региона (по умолчанию 113 — Россия): ").strip()
        if not area_str:
            area: int = 113
            break
        if area_str.isdigit() and int(area_str) > 0:
            area = int(area_str)
            break
        else:
            print("Пожалуйста, введите корректный числовой код региона.")

    return keyword, per_page, area


def user_interaction() -> None:
    """Основная функция взаимодействия с пользователем:
    - Запрашивает параметры поиска
    - Получает вакансии через API
    - Сохраняет вакансии в JSON-файл
    - Фильтрует и сортирует вакансии по ключевым словам и зарплате
    - Выводит топ N вакансий на экран"""
    api = HeadHunterAPI()
    saver = JSONSaver(PATH_TO_JSON)

    params: Optional[Tuple[str, int, int]] = get_user_input()
    if not params:
        print("Некорректный ввод параметров. Завершение работы.")
        return

    keyword, per_page, area = params

    top_n_str: str = input("Введите количество вакансий для вывода в топ N: ").strip()
    top_n: int = int(top_n_str) if top_n_str.isdigit() and int(top_n_str) > 0 else 10

    filter_words_str: str = input("Введите ключевые слова для фильтрации вакансий (через пробел): ").lower().strip()
    filter_words: List[str] = filter_words_str.split() if filter_words_str else []

    # Получаем вакансии с API
    vacancies_json = api.get_vacancies(keyword=keyword, per_page=per_page, area=area)
    vacancies_list = Vacancy.cast_to_object_list(vacancies_json)

    # Сохраняем вакансии в файл
    for vac in vacancies_list:
        try:
            saver.add_vacancy(vac)
        except Exception as e:
            print(f"Ошибка при сохранении вакансии '{vac.title}': {e}")

    # Получаем вакансии из файла для дальнейшей работы
    saved_vacancies_data = saver.get_vacancies()
    # Преобразуем словари из файла обратно в объекты Vacancy
    saved_vacancies = []
    for item in saved_vacancies_data:
        vac = Vacancy(
            title=item.get("title", ""),
            url=item.get("url", ""),
            salary=item.get("salary", ""),
            description=item.get("description", ""),
        )
        saved_vacancies.append(vac)

    # Фильтруем по ключевым словам в описании
    if filter_words:
        filtered = [vac for vac in saved_vacancies if any(word in vac.description.lower() for word in filter_words)]
    else:
        filtered = saved_vacancies

    # Сортировка по зарплате (по убыванию)
    sorted_vacancies = sorted(filtered, reverse=True)

    # Вывод топ N вакансий
    print(f"\nТоп {top_n} вакансий по зарплате:")
    for vac in sorted_vacancies[:top_n]:
        print(f"{vac.title} | {vac.salary} | {vac.url}")
        print(f"{vac.description}\n")
