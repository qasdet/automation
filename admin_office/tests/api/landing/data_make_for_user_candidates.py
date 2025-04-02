import string
import secrets

from faker import Faker

fake = Faker('ru_RU')


def name_user_candidate(name_value='Семён') -> str:
    """Имя пользователя для заявки
    Arguments:
        name_value: любое имя
    Returns:
        Имя
    """
    return name_value


def surname_user_candidate(surname_value: str) -> str:
    """Фамилия пользователя для заявки
    Arguments:
        surname_value: может принимать значения либо Юайный, либо Апишный, в зависимости от теста
    Returns:
        Фамилия
    """
    return surname_value + secrets.token_urlsafe(3)


def email_user_candidate() -> str:
    """E-mail пользователя для заявки

    Returns:
        e-mail
    """
    return fake.email()


def phone_user_candidate() -> str:
    """Телефон пользователя для заявки

    Returns:
        Телефон
    """
    return fake.lexify(text='9?????????', letters=string.digits)


def firm_name_user_candidate(firm_name_value: str) -> str:
    """Название организации
    Arguments:
        firm_name_value: может принимать значения либо 'ООО АПИ-Автотесты',
        либо 'ООО Юай-Автотесты', в зависимости от теста
    Return:
        Название организации
    """
    return firm_name_value


def comments(comments_value: str) -> str:
    """Комментарий к заявке
    Arguments:
        comments_value: комментарий, указывающий на то какой тест выполняется
    Return:
        Комментарий
    """
    return comments_value


def make_data_all_user_candidate_fields(name_value: str,
                                        surname_value: str,
                                        firm_name_value: str,
                                        comments_value: str,) -> dict:
    """Данные для всех полей заявки

    Returns:
        Словарь данных
    """

    return {
        'name': name_user_candidate(name_value),
        'surname': surname_user_candidate(surname_value),
        'firm_name': firm_name_user_candidate(firm_name_value),
        'email': email_user_candidate(),
        'phone': phone_user_candidate(),
        'comments': comments(comments_value),
        'role': 'Агентство',
    }
