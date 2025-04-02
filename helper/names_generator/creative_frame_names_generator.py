import secrets


def creative_frame_name_generator(some_user_input="CreativeFrameName") -> str:
    """ Генерирует название для рамки креатива. Только латинские буквы, цифры, подчёркивания
    Args:
        some_user_input: Пользовательский ввод названия для рамки креатива
    Returns:
        Принимает пользовательский ввод имени и добавляет к нему хэш
    """
    result = some_user_input + "_" + secrets.token_urlsafe(4).replace('-', '_')
    return result


def creative_frame_naming_generator(creative_frame_name_value: str,
                                    some_user_input="CRTVFRMNMNG") -> str:
    """ Генерирует название для рамки креатива. Только латинские буквы, цифры, подчёркивания
    Args:
        creative_frame_name_value: Имя для рамки креатива
        some_user_input: Пользовательский ввод нейминга рамки креатива
    Returns:
        Возвращает пользовательский ввод + небольшой хэш, взятый от имени рамки креатива
    """
    result = some_user_input + "_" + creative_frame_name_value.split('_')[1]
    return result
