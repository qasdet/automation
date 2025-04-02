import re

from copy import deepcopy


def search_value_coordinates(workbook_name: str, required_value: str) -> str:
    """Принимает на вход строковое значение, которое предположительно содержится в ячейке и ищет его,
    после того, как находит - возвращает координаты ячейки
    Args:
        workbook_name: название электронной таблицы, где будет проводиться операция
        required_value: строковое значение, которое нужно найти.
    Returns:
        функция возвращает адрес ячейки, в которое найдено искомое значение.
        Например 'Клиент': C4
    """
    for row in workbook_name.iter_rows(
            min_row=1, min_col=1, max_row=50, max_col=50, values_only=False
    ):
        for cell in row:
            if cell.value == required_value:
                return workbook_name.cell(
                    row=cell.row, column=cell.column
                ).coordinate


def coordinate_list_generator(
        workbook_name: str, some_input_list: list
) -> list:
    """Принимает на вход некоторый список, который содержит строковые значения, ищет их координаты и на выходе
    даёт список с координатами.
    Args:
        workbook_name: название электронной таблицы, где будет проводиться операция.
        some_input_list: список из названий, которые мы хотим найти в конкретной электронной таблице.
    Returns:
        функция возвращает адреса ячеек, в которых найдены искомые значения.
        Например: [C1, C2, C15, C19]
    """
    some_result_list = []
    for item in some_input_list:
        some_result_list.append(search_value_coordinates(workbook_name, item))
    assert len(some_input_list) == len(
        some_result_list
    ), 'Seems their length are not equal'
    return some_result_list


def list_separator(some_input_list: list) -> list:
    """Превращает список, содержащий строковые в элементы, в список, состоящий из маленьких списков.
    Args:
        some_input_list: список из строк, где каждая строка содержит адрес ячейки,
        которые мы хотим найти в конкретной электронной таблице.
    Returns:
        функция разбивает каждую строку на отдельные элементы.
        Например, было: ['C1', 'C2', 'C3']; стало: [['C', '1'],['C', '2'],['C', '3']]
    """
    ready_to_use_list = []
    for item in some_input_list:
        ready_to_use_list.append(list(re.split('(\\d+)', item)))
    for item in ready_to_use_list:
        item.pop()
    return ready_to_use_list


def to_substitute_letters(some_input_list: list) -> list:
    """Принимает на вход некоторый список с координатами и заменяет координаты со сдвигом вправо по колонке
    Например: было 'C4', а стало 'D4'"""
    subs_list = []
    united_list_with_correct_letters = []
    list_to_substitute_letters = deepcopy(some_input_list)
    for item in list_to_substitute_letters:
        next_alphabet_letter = item[0]
        ascii_var = ord(next_alphabet_letter)
        next_char = chr(ascii_var + 1)
        item[0] = next_char
        subs_list.append(item)
    for item in subs_list:
        concat_item = item[0] + item[1]
        united_list_with_correct_letters.append(concat_item)
    return united_list_with_correct_letters


def to_substitute_numbers(some_input_list: list, shift_number: int) -> list:
    """Принимает на вход некоторый список с координатами и заменяет координаты со сдвигом вниз по строке
    Например: было 'E2', а стало 'E10'
    """
    subs_list = []
    united_list_with_correct_letters = []
    list_to_substitute_numbers = deepcopy(some_input_list)
    for item in list_to_substitute_numbers:
        item = re.split('(\\d+)', item)[:-1]
        next_required_number = int(item[1]) + shift_number
        item[1] = str(next_required_number)
        subs_list.append(item)
    for item in subs_list:
        concat_item = item[0] + item[1]
        united_list_with_correct_letters.append(concat_item)
    return united_list_with_correct_letters


def find_names_by_coordinates(workbook_name: str, list_to_input: list) -> list:
    """Принимает на вход список координат, а возвращает список значений,
    которые содержатся в ячейках по этим адресам
        Args:
            workbook_name: название электронной таблицы, где будет проводиться операция.
            list_to_input: список из строк, которые содержат координаты ячеек.
        Returns:
            ищет ячейку по её адресу и возвращает значение ячейки
            Например D4: Hyundai
    """
    result_list = []
    for item in list_to_input:
        result_list.append(workbook_name[item].value)
    return result_list
