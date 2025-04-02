def compare_lists_of_dictionaries(list1: list, list2: list) -> list | bool:
    differences_list = []
    for each_record in list1:
        if each_record not in list2:
            differences_list.append(each_record)
    if len(differences_list) == 0:
        return True
    elif len(differences_list) > 0:
        return differences_list


def get_key_from_dict_by_value(some_dict, some_value):
    """
    Принимает на вход словарь и значение какого-либо элемента.
    Возвращает ключ для указанного элемента
    """
    result = list(some_dict.keys())[list(some_dict.values()).index(some_value)]
    return result


def remove_keys_from_dict(dict_to_use: dict, removal_list: list) -> dict:
    """Удаляет n кол-во ключей в словаре
        Args:
            dict_to_use: Словарь, в котором нужно удалить ключи
            removal_list: Список ключей, которые надо удалить
        Returns:
            Словарь, без ключей, которые мы удалили
    """
    for element in removal_list:
        dict_to_use.pop(element, None)


def set_timezone_for_records_in_dict(dict_to_edit: dict, dict_key, value_to_find='T', time_zone_value=3):
    """Находит нужные ключи из списка и редактирует формат времени и даты
        Args:
            dict_to_edit: Словарь, в котором отредактировать ключи
            dict_key: Ключ, значение в котором надо редактировать
            value_to_find: От какого значения в строке искать
            time_zone_value: Значение для часового пояса
        Returns:
            Отредактированную
    """
    get_the_hours_position = int(dict_to_edit[dict_key].find(value_to_find))
    required_position_start = get_the_hours_position + 1
    required_position_end = get_the_hours_position + 3
    get_the_old_hours_value = int(dict_to_edit[dict_key][
                                  required_position_start:required_position_end])
    get_the_new_hours_value = get_the_old_hours_value - time_zone_value
    if len(str(get_the_new_hours_value)) == 1:
        get_the_new_hours_value = "0" + str(get_the_new_hours_value)
    test_var = dict_to_edit[dict_key].replace(value_to_find + str(get_the_old_hours_value),
                                              value_to_find + str(get_the_new_hours_value))
    return test_var


def get_difference_between_two_dictionaries(
    first_dict: dict, second_dict: dict
) -> (str, dict):
    """Сравнение двух словарей на равенство
    Args:
        first_dict: словарь данных записи
        second_dict: словарь данных записи

    Returns:
        Возвращаем ожидаемый ответ от сервиса и сообщение для assert
    """
    if first_dict.keys() == second_dict.keys():
        difference = {
            f'{key}': f'ФР: {first_dict[key]}  ОР: {second_dict[key]}'
            for key, value in second_dict.items()
            if value != first_dict[key]
        }
        message = 'Значения полей не совпадают'
    else:
        difference = set(first_dict.keys()) ^ set(second_dict.keys())
        message = 'Количество полей не совпадают'
    return message, difference


def compare_the_response_from_service_with_expected_response(
    response_data: dict, data_source: dict
) -> None:
    """Проверяем данные от сервиса
    Args:
        response_data: ответ от сервиса
        data_source: ожидаемый ответ от сервиса
    """
    message, difference = get_difference_between_two_dictionaries(
        response_data, data_source
    )
    assert (
        not difference
    ), f'Ответ от сервиса не равен ожидаемому. {message}. Разница {difference}'


def create_dictionary_from_list(some_list: list) -> dict:
    """ На вход даётся список, на выходе получается словарь
        Args:
            some_list: список строк, в котором каждый элемент состоит из строки, которую надо разделить на два элемента.
        Returns:
            Словарь, где левый элемент из бывшего списка будет ключом, а правый - значением.
            Например: ['utm_mts=1fxjq8000', 'utm_source=ydirect', 'utm_medium=dis_cpm'], превращается в
            {'utm_mts': '1fxjq8000', 'utm_source': 'ydirect', 'utm_medium': 'dis_cpm',
    """
    some_dictionary = {}
    for item in some_list:
        some_dictionary[item.split('=')[0]] = item.split('=')[1]
    return some_dictionary
