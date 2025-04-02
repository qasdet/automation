import secrets
import re

from datetime import datetime


def advertising_campaign_name_generator(some_user_input="Тест") -> str:
    """ Вводится строка для названия РК. Так как функция может использоваться в разных местах и для разных РК, я
    добавил возможность указывать строку

    Args:
        some_user_input: Пользовательский ввод названия рекламной кампании

    Returns:
        Проверяет, что ввод кириллический, добавляет текущую дату и время без разделителей. С одной стороны, это даёт
        надежду, что название точно уникальное, с другой стороны, даёт возможность понять, когда точно сгенерировалось
        название.
    """
    assert bool(re.search("[\u0400-\u04FF]", some_user_input)), "Название рекламной кампании должно быть на русском"
    datetime_value = str(datetime.now().strftime("%Y%m%d%H%M%S"))
    result = some_user_input + "РеклКамп" + datetime_value
    return result


def advertising_campaign_code_generator(some_user_input="ADVCD") -> str:
    """ Цифры, латинские буквы, 3-15 символов, первый символ не должен быть дефисом.

    Args:
        some_user_input: Пользовательский ввод названия рекламной кампании

    Returns:
        Проверяет строку на наличие гласных, как строчных, так и заглавных. Удаляет все, которые находит. Возвращает,
        что осталось.
    """
    assert 3 <= len(some_user_input) < 8, "Введённое значение не соответствует требованиям, от 3 до 8 символов"
    assert bool(re.search("[a-zA-Z]", some_user_input)), "Код рекламной кампании должен быть на латинице"
    assert some_user_input[0] != '-', "Код рекламной кампании начинается не с дефиса"
    time_value = str(datetime.now().strftime("%H%M%S"))
    result = some_user_input + time_value + secrets.token_urlsafe(2).replace('_', '-')
    assert 3 < len(result) <= 15, "Итоговое значение не соответствует требованиям, от 3 до 15 символов"
    return result
