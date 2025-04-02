from copy import deepcopy
from datetime import datetime
from faker import Faker
from admin_office.tests.api.organizations.data_generator_for_organization import (
    address_organization,
    email_organization,
    inn_generator,
    kpp_generator,
    name_organization,
    ogrn_generator,
    phone_organization,
)
from admin_office.constants import ORGANIZATION_STATUS_NEW

fake = Faker('ru_RU')


def make_data_for_required_individual_entrepreneur_fields() -> dict:
    """Данные для обязательных полей для ИП

    Returns:
        Возвращаем словарь данных
    """
    name = name_organization()
    return {
        'roleCode': 'agency',
        'fullName': f'Индивидуальный предприниматель {name}',
        'shortName': f'ИП {name}',
        'inn': inn_generator(12),
        'email': email_organization(),
        'okopf': None,
        'firmName': None,
        'ogrn': None,
        'address': None,
        'phone': None,
        'kpp': None,
    }


def make_data_all_individual_entrepreneur_fields() -> dict:
    """Данные для всех поля для ИП

    Returns:
        Возвращаем словарь данных
    """
    data_for_organization = (
        make_data_for_required_individual_entrepreneur_fields()
    )
    data_for_organization.update(
        {
            'okopf': 'Индивидуальный предприниматель',
            'firmName': data_for_organization['shortName'],
            'ogrn': ogrn_generator(15),
            'address': address_organization(),
            'phone': phone_organization(),
        }
    )
    return data_for_organization


def make_data_for_required_legal_entity_fields() -> dict:
    """Данные для обязательных полей для юр. лица

    Returns:
        Возвращаем словарь данных
    """
    name = name_organization()
    return {
        'roleCode': "agency",
        'fullName': f'ООО {name}',
        'shortName': f'ООО {name}',
        'inn': inn_generator(10),
        'kpp': kpp_generator(),
        'email': email_organization(),
        'okopf': None,
        'firmName': None,
        'ogrn': None,
        'address': None,
        'phone': None,
    }


def make_data_all_legal_entity_fields() -> dict:
    """Данные для всех поля для юр. лица

    Returns:
        Возвращаем словарь данных
    """
    data_for_organization = make_data_for_required_legal_entity_fields()
    data_for_organization.update(
        {
            'okopf': 'Общество с ограниченной ответственностью',
            'firmName': data_for_organization['shortName'],
            'ogrn': ogrn_generator(13),
            'address': address_organization(),
            'phone': phone_organization(),
        }
    )
    return data_for_organization


def make_the_expected_response(
    organization_id: int, organization_data: dict, registered_at: str = None
) -> dict:
    """Ожидаемый ответ от сервиса
    Args:
        organization_id: id записи
        organization_data: данные организации, которые отправлены в запрос
        registered_at: дата создания организации

    Returns:
        Возвращаем словарь данных
    """
    expected_response = deepcopy(organization_data)
    expected_response.update(
        {
            'id': organization_id,
            '__typename': 'Organization',
            'registeredAt': registered_at
            if registered_at
            else datetime.now().strftime('%Y-%m-%dT%H:%M'),
            'blockedAt': None,
            'role': organization_data['roleCode'],
            'status': 'new',
        }
    )
    expected_response.pop('roleCode')
    return expected_response


def make_the_expected_data_for_ui(organization_data: dict) -> dict:
    """Ожидаемые данные для добавленной организации через ui

    Args:
        organization_data: данные организации, при создании через UI

    Returns:
        Словарь данных
    """
    expected_data = deepcopy(organization_data)
    expected_data.update(
        {'registered_at': datetime.now().strftime('%d.%m.%Y %H:%M')}
    )
    expected_data.update({'status': ORGANIZATION_STATUS_NEW})
    return expected_data
