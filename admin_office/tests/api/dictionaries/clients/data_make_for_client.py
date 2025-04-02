import secrets

from admin_office.constants import ORGANIZATION
from admin_office.tests.api.organizations.data_generator_for_organization import (
    inn_generator,
    kpp_generator
)
from db_stuff.db_interactions.clients_db_interactions import get_client_by_naming


unique_hash = secrets.token_urlsafe(3).replace('_', '-')


def client_name() -> str:
    """Название клиента

    Returns:
        Название клиента
    """
    # Чтобы запись была в первой строке таблицы
    return f"1_AT_ИмяКлиента_" + unique_hash


def client_full_name() -> str:
    """Название клиента

    Returns:
        Название клиента
    """
    return f"1_AT_ПолноеИмяКлиента_" + unique_hash


def client_naming() -> str:
    """Нейминг клиента

    Returns:
        Нейминг клиента
    """
    return f"AT-clnt-namng-" + unique_hash


def make_data_all_client_fields() -> dict:
    """Данные для всех полей клиента

    Returns:
        Словарь данных
    """
    name = client_name()
    naming = client_naming()
    full_name = client_full_name()
    inn = inn_generator()
    kpp = kpp_generator()
    return {
        'name': name,
        'naming': naming,
        'fullName': full_name,
        'inn': inn,
        'kpp': kpp,
        'organization': ORGANIZATION,
    }


def make_the_expected_data_for_ui(client_data: dict) -> dict:
    """Ожидаемые данные для добавленного клиента через ui

    Args:
        client_data: данные клиента, при создании через UI

    Returns:
        Словарь данных
    """
    client_data.update(get_client_by_naming(client_data['naming']))
    return client_data
