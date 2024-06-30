
import csv

FILENAME = "housing_data.csv"

HOUSE_TYPE_MIN_1 = 0
HOUSE_TYPE_MIN_2 = 5
HOUSE_TYPE_MIN_3 = 15


def read_file(filename: str) -> list[dict]:
    """Читает данные из CSV файла и преобразует их в список словарей.

    :param filename: Название файла, содержащего данные.
    :return: Список словарей с данными о домах.
    """
    with open(filename, encoding="utf-8") as file:
        reader = list(csv.DictReader(file))
        list_dict = list(reader)
        for row in list_dict:
            row["floor_count"] = int(row["floor_count"])
            row["population"] = int(row["population"])
            row["heating_value"] = float(row["heating_value"])
            row["area_residential"] = float(row["area_residential"])
        return list_dict


def classify_house(floor_count: int) -> str:
    """Классифицирует дом на основе количества этажей.

    Проверяет, является ли количество этажей целым числом и положительным значением.
    Возвращает категорию дома в зависимости от количества этажей.

    :param floor_count: Количество этажей в доме.
    :return: Категория дома в виде строки: "Малоэтажный", "Среднеэтажный" или "Многоэтажный".
    """
    if not isinstance(floor_count, int):
        raise TypeError  # Количество этажей должно быть целым числом
    if not floor_count > HOUSE_TYPE_MIN_1:
        raise ValueError  # Количество этажей должно быть положительным
    if HOUSE_TYPE_MIN_1 < floor_count <= HOUSE_TYPE_MIN_2:
        house_type = "Малоэтажный"
    elif HOUSE_TYPE_MIN_2 < floor_count <= HOUSE_TYPE_MIN_3:
        house_type = "Среднеэтажный"
    else:
        house_type = "Многоэтажный"
    return house_type


def get_classify_houses(houses: list[dict]) -> list[str]:
    """Классифицирует дома на основе количества этажей.

    :param houses: Список словарей с данными о домах.
    :return: Список категорий домов.
    """
    return [classify_house(house["floor_count"]) for house in houses]


def get_count_house_categories(categories: list[str]) -> dict[str, int]:
    """
    Подсчитывает количество домов в каждой категории.

    :param categories: Список категорий домов.
    :return: Словарь с количеством домов в каждой категории.
    """
    return {
        "Малоэтажный": categories.count("Малоэтажный"),
        "Среднеэтажный": categories.count("Среднеэтажный"),
        "Многоэтажный": categories.count("Многоэтажный"),
    }


def min_area_residential(houses: list[dict]) -> str:
    """Находит адрес дома с наименьшим средним количеством квадратных метров жилой площади на одного жильца.

    :param houses: Список словарей с данными о домах.
    :return: Адрес дома с наименьшим средним количеством квадратных метров жилой площади на одного жильца.
    """
    area_per_person_dict = {
        house["house_address"]: round((house["area_residential"] / house["population"]), 2) for house in houses
    }
    min_house_address = None
    min_area_per_person = float("inf")
    for house in area_per_person_dict:
        area_per_person = area_per_person_dict[house]
        if area_per_person < min_area_per_person:
            min_area_per_person = area_per_person
            min_house_address = house
    return min_house_address


if __name__ == "__main__":
    print(f"Результат категоризации домов:\n{get_count_house_categories(get_classify_houses(read_file(FILENAME)))}")
    print(f"Дом с наименьшей средней жилой площадью на одного жильца:\n{min_area_residential(read_file(FILENAME))}")
