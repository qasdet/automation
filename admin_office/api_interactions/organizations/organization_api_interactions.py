from datetime import datetime
from faker import Faker
from http_methods.post import post_request
from db_stuff.db_interactions.organizations_db_interactions import Organizations
from db_stuff.sqlalchmy_interactions import establish_postgresql_connection

fake = Faker('ru_RU')

DEV_GRAPHQL = 'https://dev-graphql.mediapush.mts-corp.ru/'

GET_ORGANIZATIONS_LIST_QUERY = {
    'operation_name': 'Organizations',
    'query': 'query Organizations($id: ID, $slice: UserOfficeSlice, $filter: OrganizationFilter, '
    '$sort: OrganizationSort) {organizations(id: $id, slice: $slice, filter: $filter, sort: $sort) { '
    '...OrganizationBase}}',
    'fragment': 'fragment OrganizationBase on Organization {id fullName}',
}


def get_organizations_list(some_query: dict, some_token: str) -> dict:
    some_result = post_request(some_query, some_token).json
    return some_result


def get_organization_id(
    organization_name: str, organizations_list: list
) -> str:
    """На вход функция принимает имя организации и словарь со списком имён и всех организаций.
    Возвращает айди искомой нами организации"""
    for item in organizations_list['data']['organizations']:
        if item['fullName'] == organization_name:
            return item['id']


FRAGMENT = (
    'fragment OrganizationBase on Organization {'
    '  id'
    '  role'
    '  status'
    '  ogrn'
    '  okopf'
    '  fullName'
    '  firmName'
    '  shortName'
    '  inn'
    '  kpp'
    '  address'
    '  phone'
    '  email'
    '  registeredAt'
    '  blockedAt'
    '}'
)


def formatted_date_without_timezone(date: str):
    """Формируем дату без timezone"""
    return datetime.strptime(date[:25], '%Y-%m-%dT%H:%M:%S.%f').strftime(
        '%Y-%m-%dT%H:%M'
    )


def formatted_phone(phone: str) -> str:
    """Приводим номер телефона к единому формату"""
    return (
        phone.replace('+7', '')
        .replace(' ', '')
        .replace(')', '')
        .replace('(', '')
    )


def create_organization(
    token: str, data_organization: dict, with_error: bool = False
) -> dict:
    """Создаем запись
    Args:
        data_organization: словарь данных
        with_error: False - проверять, что запрос выполнен без ошибок,
                    True - Проверям, что запрос выполнен с ошибками
    Returns:
        Возвращается сроварь данных новой записи
    """
    query = {
        'operationName': 'adminOrganizationCreate',
        'variables': {'data': data_organization},
        'query': 'mutation adminOrganizationCreate($data: OrganizationData!) {'
        '  adminOrganizationCreate(data: $data) {'
        '    ...OrganizationBase'
        '    __typename'
        '  }'
        '}' + FRAGMENT,
    }
    if with_error:
        return post_request(query, token, with_errors=with_error).get('errors')
    else:
        return post_request(query, token)['data']['adminOrganizationCreate']


def edit_organization(
    token: str,
    organization_id: int,
    data_organization: dict,
    with_error: bool = False,
) -> dict:
    """Редактируем запись с указанным id
    Args:
        organization_id: id записи
        data_organization: словарь новых данных
        with_error: False - проверять, что запрос выполнен без ошибок,
                    True - Проверям, что запрос выполнен с ошибками
    Returns:
        Возвращается сроварь данных указанной записи
    """
    query = {
        'operationName': 'adminOrganizationUpdate',
        'variables': {'id': organization_id, 'data': data_organization},
        'query': 'mutation adminOrganizationUpdate($id: ID!, $data: OrganizationData!) {'
        '  adminOrganizationUpdate(id: $id, data: $data) {'
        '    ...OrganizationBase'
        '    __typename'
        '  }'
        '}' + FRAGMENT,
    }
    if with_error:
        return post_request(query, token, with_errors=with_error).get('errors')
    else:
        return post_request(query, token)['data']['adminOrganizationUpdate']


def activate_organization(token, organization_id: int) -> dict:
    """Активируем запись с указанным id
    Args:
        organization_id: id записи
    Returns:
        Возвращается сроварь данных указанной записи
    """
    query = {
        'operationName': 'adminOrganizationActivate',
        'variables': {'id': organization_id},
        'query': 'mutation adminOrganizationActivate($id: ID!) {'
        '  adminOrganizationActivate(id: $id) {'
        '    ...OrganizationBase'
        '    __typename'
        '  }'
        '}' + FRAGMENT,
    }
    return post_request(query, token)['data']['adminOrganizationActivate']


def blocked_organization(token: str, organization_id: int) -> dict:
    """Блокируем запись с указанным id
    Args:
        organization_id: id записи
    Returns:
        Возвращается сроварь данных указанной записи
    """
    query = {
        'operationName': 'adminOrganizationBlock',
        'variables': {'id': organization_id},
        'query': 'mutation adminOrganizationBlock($id: ID!) {'
        '  adminOrganizationBlock(id: $id) {'
        '    ...OrganizationBase'
        '    __typename'
        '  }'
        '}' + FRAGMENT,
    }
    return post_request(query, token)['data']['adminOrganizationBlock']


def get_organization_by_id(token, organization_id: int) -> dict:
    """Получить запись с указанным id
    Args:
        organization_id: словарь данных записи
    Returns:
        Возвращается сроварь данных указанной записи
    """
    query = {
        'variables': {'id': organization_id},
        'query': 'query adminOrganizations($id: ID!) {'
        '  adminOrganizations(id: $id) {'
        '    ...OrganizationBase'
        '    __typename'
        '  }'
        '}' + FRAGMENT,
    }
    return post_request(query, token)['data']['adminOrganizations']


def get_specified_amount_of_organizations(token, amount: int = 2):
    """Получить указанное количество записей отсортированных по статусу
    Args:
        amount: словарь данных записи
    Returns:
        Возвращается список из записей
    """
    query = {
        'variables': {
            'slice': {'limit': amount, 'offset': 0},
            'sort': {'direction': 'asc', 'field': 'status'},
        },
        'query': 'query adminOrganizations('
        ' $id: ID, $slice: ListSlice, $filter: OrganizationFilter, $sort: OrganizationSort) {'
        ' adminOrganizations(id: $id, slice: $slice, filter: $filter, sort: $sort) {'
        '    ...OrganizationBase'
        '  }'
        '}' + FRAGMENT,
    }

    rows = post_request(query, token)['data']['adminOrganizations']
    return [
        {
            'id': row['id'],
            'role': row['role'],
            'status': row['status'],
            'okopf': row['okopf'],
            'fullName': row['fullName'],
            'shortName': row['shortName'],
            'firmName': row['firmName'],
            'inn': row['inn'],
            'ogrn': row['ogrn'],
            'kpp': row['kpp'],
            'address': row['address'],
            'phone': row['phone'],
            'email': row['email'],
            'registeredAt': datetime.strptime(row['registeredAt'], '%Y-%m-%dT%H:%M:%S.%f%z'
                                 ).strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
            'blockedAt': row['blockedAt'],
        }
        for row in rows
    ]


def get_count_of_organizations(token: str) -> int:
    """Получить указанное количество записей
    Args:
        token: токен доступа
    Returns:
        Возвращается количество записей
    """
    query = {
        'query': 'query adminOrganizations('
        ' $id: ID, $slice: UserOfficeSlice, $filter: OrganizationFilter, $sort: OrganizationSort) {'
        ' adminOrganizations(id: $id, slice: $slice, filter: $filter, sort: $sort) {'
        '    ...OrganizationBase'
        '    __typename'
        '  }'
        '}' + FRAGMENT,
    }
    rows = post_request(query, token)['data']['adminOrganizations']
    return len(rows)


def get_specified_amount_of_organizations_from_db(amount: int = 2) -> list:
    """Получить указанное количество записей отсортированных по статусу из БД
    Args:
        amount: словарь данных записи
    Returns:
        Возвращается список из записей
    """
    session = establish_postgresql_connection()
    rows = (
        session.query(Organizations)
        .order_by(Organizations.status)
        .limit(amount)
        .all()
    )
    session.close()
    return [
        {
            'id': str(row.id),
            'role': row.role,
            'status': row.status,
            'ogrn': row.ogrn,
            'okopf': row.okopf,
            'fullName': row.full_name,
            'firmName': row.firm_name,
            'shortName': row.short_name,
            'inn': row.inn,
            'kpp': row.kpp,
            'address': row.address,
            'phone': row.phone,
            'email': row.email,
            'registeredAt': row.registered_at.strftime('%Y-%m-%dT%H:%M:%S.%f%z'),
            'blockedAt': row.blocked_at,
        }
        for row in rows
    ]