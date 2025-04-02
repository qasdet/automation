def name_generator(unique_hash_value: str) -> str:
    return 'atsourcename' + unique_hash_value


def short_name_generator(unique_hash_value: str) -> str:
    """ Не больше 15 символов """
    return 'atsrcshnm' + unique_hash_value


def naming_generator(unique_hash_value: str) -> str:
    """ Только латинские символы, цифры и тире """
    return 'atsrcnaming' + unique_hash_value


def url_generator(url_value='https://yandex.ru') -> str:
    return url_value


def code_generator(unique_hash_value: str) -> str:
    """Не больше 8 символов"""
    return 'atcd' + unique_hash_value
