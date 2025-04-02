from faker import Faker
from http_methods.post import post_request

fake = Faker()


def get_channels_api(admin_office_token: str) -> list:
    """ Отправка запроса на сервер для получения списка каналов
    Args:
        admin_office_token: токен авторизации в admin-office
    Returns:
        Словарь, содержащий все имена каналов
    """
    get_channels_query = {
        'operation_name': 'Channels',
        'query': 'query {adminChannels {name code mediaType isUsedBySplan naming}}'}
    result = post_request(get_channels_query, admin_office_token)
    return result['data']['adminChannels']


def get_specific_channel_by_code_api(code_value: str, token: str) -> dict:
    """ Получить данные по конкретному каналу

    Args:
        code_value: код, созданного канала
        token: токен, для авторизации на сервер
    Returns:
        Словарь, содержащий данные по какому-то конкретному каналу
    """
    get_specific_channel = {
        'variables': {
            "code": f"{code_value}"
        },
        'query': 'query AdminChannels ($code: ID!,'
                 ' $slice: UserOfficeSlice, '
                 '$filter: ChannelFilter) {'
                 'adminChannels('
                 'code: $code, '
                 'slice: $slice, '
                 'filter: $filter) '
                 '{...Channel}}'
                 'fragment Channel on Channel {'
                 '  name'
                 '  code'
                 '  naming'
                 '  mediaType'
                 '  isUsedBySplan'
                 '}',
    }
    return post_request(get_specific_channel, token)


def create_channel_api(
        name: str,
        code: str,
        naming: str,
        media_type: str,
        is_used_by_splan: bool,
        token: str,
        with_errors: bool = False,
) -> dict:
    """Создание канала

    Args:
        name: название канала
        code: код канала
        naming: нейминг
        media_type: категория медиа
        is_used_by_splan: Используется в страт. плане
        token: токен доступа
        with_errors: False - проверять, что запрос выполнен без ошибок,
                     True - Проверяем, что запрос выполнен с ошибками
    Returns:
        Созданная запись
    """
    create_channel_query = {
        'variables': {
            'data': {
                'name': name,
                'code': code,
                'naming': naming,
                'mediaType': media_type,
                'isUsedBySplan': is_used_by_splan,
            }
        },
        'query': 'mutation adminChannelCreate($data: ChannelCreateData!) {'
                 '  adminChannelCreate(data: $data) {'
                 '    ...Channel'
                 '  }'
                 '}'
                 'fragment Channel on Channel {'
                 '  name'
                 '  code'
                 '  naming'
                 '  mediaType'
                 '  isUsedBySplan'
                 '}',
    }
    return post_request(create_channel_query, token, with_errors)


def edit_channel_api(
        code: str,
        name: str,
        naming: str,
        media_type: str,
        is_used_by_splan: bool,
        token: str,
) -> dict:
    """Редактирование канала

    Args:
        name: название канала
        code: код канала
        naming: нейминг канала
        token: токен доступа
        media_type: категория медиа
        is_used_by_splan: Используется в страт. плане
    Returns:
        Отредактированная запись
    """
    update_channel_query = {
        'variables': {
            'code': code,
            'data': {
                'name': name,
                'naming': naming,
                'mediaType': media_type,
                'isUsedBySplan': is_used_by_splan,
            },
        },
        'query': 'mutation adminChannelUpdate($code: ID!, $data: ChannelUpdateData!) {'
                 '  adminChannelUpdate(code: $code, data: $data) {'
                 '    ...Channel'
                 '  }'
                 '}'
                 'fragment Channel on Channel {'
                 '  code'
                 '  name'
                 '  naming'
                 '  mediaType'
                 '  isUsedBySplan'
                 '}',
    }
    response = post_request(update_channel_query, token)['data'][
        'adminChannelUpdate'
    ]
    return response
