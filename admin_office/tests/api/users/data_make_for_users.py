import string
import secrets

from copy import deepcopy
from faker import Faker
from admin_office.constants import ORGANIZATION, USER_STATUS_NEW, AUTOTEST_USER_PREFIX

fake = Faker('ru_RU')
USER_ROLE = 'Медиапланер (диджитал)'
unique_hash = secrets.token_urlsafe(3)


def name_user(hash_value: str) -> str:
    """Имя пользователя

    Returns:
        Имя пользователя
    """
    generated_name = 'Иван_' + AUTOTEST_USER_PREFIX + '_' + hash_value
    return generated_name


def surname_user(hash_value: str) -> str:
    """Фамилия пользователя

    Returns:
        Фамилия пользователя
    """
    generated_name = 'Иванов_' + AUTOTEST_USER_PREFIX + '_' + hash_value
    return generated_name


def middle_name_user(hash_value: str) -> str:
    """Отчество пользователя

    Returns:
        Отчество пользователя
    """
    generated_name = 'Иванович_' + AUTOTEST_USER_PREFIX + '_' + hash_value
    return generated_name


def email_user(some_unique_value) -> str:
    """e-mail пользователя

    Returns:
        e-mail в виде строки
    """
    return some_unique_value + '@mailprovider.ru'


def login_user(some_unique_value) -> str:
    """Логин пользователя

    Returns:
        login в виде строки
    """
    return 'at_' + some_unique_value


def phone_user() -> str:
    """Телефон пользователя

    Returns:
       Телефон в виде строки
    """
    return fake.lexify(text='9?????????', letters=string.digits)


def contact_phone_user() -> str:
    """Контактный Телефон пользователя

    Returns:
        Телефон в виде строки
    """
    return fake.lexify(text='9?? ??? ?? ??', letters=string.digits)


def make_data_all_user_fields() -> dict:
    """Данные для всех полей пользователя

    Returns:
        Словарь данных
    """
    name = name_user(unique_hash)
    middle_name = middle_name_user(unique_hash)
    surname = surname_user(unique_hash)
    email = email_user(name.split('_')[-1])
    login = login_user(name.split('_')[-1])

    return {
        'name': name,
        'middle_name': middle_name,
        'surname': surname,
        'email': email,
        'login': login,
        'phone': phone_user(),
        'contact_phone': contact_phone_user(),
        'role': USER_ROLE,
        'organization': ORGANIZATION,
    }


def make_the_expected_data_for_ui(user_data: dict) -> dict:
    """Ожидаемые данные для добавленного пользователя через ui

    Args:
        user_data: данные организации, при создании через UI

    Returns:
        Словарь данных
    """
    expected_data = deepcopy(user_data)
    expected_data.update({'status': USER_STATUS_NEW})
    return expected_data
