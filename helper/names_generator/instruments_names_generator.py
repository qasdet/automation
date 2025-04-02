def tools_name_generator(unique_hash_value: str) -> str:
    """ Генерация имени инструмента """
    return 'attoolname' + unique_hash_value


def tools_short_name_generator(unique_hash_value: str) -> str:
    """ Генерация короткого имени инструмента. Не больше 15 символов """
    return 'attoolshnm' + unique_hash_value


def tools_naming_generator(unique_hash_value: str) -> str:
    """ Генерация нейминга инструмента. Только латинские символы, цифры и тире """
    return 'attoolnaming' + unique_hash_value


def tools_url_generator(url_value='https://yandex.ru') -> str:
    """ Подстановка урла """
    return url_value


def tools_code_generator(unique_hash_value: str) -> str:
    """Генерация кода инструмента. Не больше 8 символов"""
    return 'attl' + unique_hash_value
