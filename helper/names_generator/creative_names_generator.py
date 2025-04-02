import secrets


def creative_name_generator(some_user_input="CreativeName") -> str:
    """ Генерирует название для рамки креатива. Только латинские буквы, цифры, подчёркивания
    Args:
        some_user_input: Пользовательский ввод названия креатива
    Returns:
        Возвращает пользовательский ввод + небольшой хэш
    """
    result = some_user_input + "_" + secrets.token_urlsafe(4).replace('-', '_')
    return result


def creative_naming_generator(creative_name_value: str,
                              some_user_input="CRTVNMNG") -> str:
    """ Генерирует название для креатива. Только латинские буквы, цифры, подчёркивания
    Args:
        creative_name_value: Имя для креатива
        some_user_input: Пользовательский ввод нейминга креатива
    Returns:
        Возвращает пользовательский ввод + небольшой хэш, взятый от имени креатива
    """
    result = some_user_input + "_" + creative_name_value.split('_')[1]
    return result
