import secrets

from copy import deepcopy
from faker import Faker
from admin_office.constants import CHANNEL_PREFIX

fake = Faker()


def generate_channel_name() -> str:
    """Метод создания имени канала"""
    generated_name = CHANNEL_PREFIX + '_' + secrets.token_urlsafe(4).lower().replace('_', '').replace('-', '')
    return generated_name


def generate_channel_code(channel_name_value: str, part_should_be_stripped: str) -> str:
    """Метод создания кода канала
    Arguments
        channel_name_value: имя канала
        part_should_be_stripped: та часть, которая будет отрезана от имени канала
    Returns
        Вернёт уникальный хэш из четырёх символов. Такой же хэш содержится в имени канала.
    """
    return channel_name_value.lstrip(part_should_be_stripped)


def generate_channel_naming(channel_name_value: str, part_should_be_stripped: str) -> str:
    """Метод создания нейминга канала
    Arguments
        channel_name_value: имя канала
        part_should_be_stripped: та часть, которая будет отрезана от имени канала
    Returns
        Вернёт уникальный хэш из четырёх символов и добавит к нему слово 'naming'.
        Такой же хэш содержится в имени канала.
    """
    return channel_name_value.lstrip(part_should_be_stripped) + '-naming'


def get_data_for_channel() -> dict:
    """Данные канала"""
    channel_name = generate_channel_name()
    channel_code = generate_channel_code(channel_name, CHANNEL_PREFIX)
    channel_naming = generate_channel_naming(channel_name, CHANNEL_PREFIX)
    return {
        'name': channel_name,
        'code': channel_code,
        'naming': channel_naming,
        'media_type': 'TV',
        'is_used_by_splan': False,
    }


def make_the_expected_response_for_channel(
        id_channel: int, data_channel: dict
) -> dict:
    """Ожидаемые данные"""
    expected_data = deepcopy(data_channel)
    expected_data.update({'id': id_channel, '__typename': 'Channel'})
    return expected_data
