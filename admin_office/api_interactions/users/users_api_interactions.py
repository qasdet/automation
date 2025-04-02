from requests.exceptions import ConnectionError
from http_methods.post import post_request


def get_users(token: str) -> list:
    """ Получить список пользователей в Admin Office

    Args:
        token: токен, для авторизации на сервер
    Returns:
        Словарь, содержащий список пользователей
    """
    get_users_query = {
        'variables': {},
        'query': 'query AdminProfiles {adminProfiles { user {...UserBase}}}'
                 'fragment UserBase on User '
                 '{id status login email phone registeredAt blockedAt}',
    }
    result = post_request(get_users_query, token)['data']['adminProfiles']
    ready_to_use_list = []
    for each_item in result:
        ready_to_use_list.append(each_item['user'])
    return ready_to_use_list


def get_persons(token: str) -> list:
    """ Получить список пользователей в Admin Office

    Args:
        token: токен, для авторизации на сервер
    Returns:
        Словарь, содержащий список пользователей
    """
    get_persons_query = {
        'variables': {},
        'query': 'query AdminProfiles {adminProfiles { person {...PersonBase}}}'
                 'fragment PersonBase on Person '
                 '{id organizationID surname name middleName contactPhone}',
    }
    result = post_request(get_persons_query, token)['data']['adminProfiles']
    ready_to_use_list = []
    for each_item in result:
        ready_to_use_list.append(each_item['person'])
    return ready_to_use_list


def get_users_attribute(users_list: list, field: str) -> list:
    """
    Получение списка какого-то одного поля по всем юзерам
        Args:
            users_list: список юзеров
            field: колонка, по которой мы хотим получить выборку
        Returns:
            Возвращает список, состоящий из какого-то одного поля, например список уникальных идентификаторов
    """
    ids_list = []
    for item in users_list:
        ids_list.append(item.get(field))
    return ids_list


def get_persons_attribute(persons_list: list, field: str) -> list:
    """
    Получение списка какого-то одного поля по всем пользователям
        Args:
            persons_list: список юзеров
            field: колонка, по которой мы хотим получить выборку
        Returns:
            Возвращает список, состоящий из какого-то одного поля, например список уникальных идентификаторов
    """
    ids_list = []
    for item in persons_list:
        ids_list.append(item.get(field))
    return ids_list


def get_user_by_id(id_value: str, token: str) -> dict | bool:
    """
    Получение данных пользователя по уникальному номеру
        Args:
            id_value: уникальный идентификатор
            token: токен авторизации
        Returns:
            Возвращает словарь с данными по профилю пользователя (из таблицы users и persons)
    """
    try:
        get_user_query = {
            'operationName': 'adminProfiles',
            'variables': {'id': f'{id_value}'},
            'query': 'query adminProfiles($id: ID!) {adminProfiles(id: $id) {user {id status} person {id name}}}'
        }
        result = post_request(get_user_query, token)
        return result
    except (ConnectionError, NameError):
        return False


def create_user(name: str,
                surname: str,
                organization_id: str,
                login: str,
                email: str,
                phone: str,
                token: str) -> dict | bool:
    """
    Создание пользователя
        Args:
            name: имя пользователя
            surname: фамилия пользователя
            organization_id: уникальный номер организации
            login: логин пользователя
            email: почта пользователя
            phone: телефон пользователя
            token: токен авторизации
        Returns:
            Возвращает словарь с данными по профилю созданного пользователя
    """
    try:
        create_user_query = {
            'operation_name': 'adminProfileCreate',
            'variables': {
                'name': f'{name}',
                'surname': f'{surname}',
                'organizationID': f'{organization_id}',
                'login': f'{login}',
                'email': f'{email}',
                'phone': f'{phone}',
            },
            'query': 'mutation adminProfileCreate ($name: String, $surname: String, $organizationID: ID!, '
                     '$login: String!, $email: String!, $phone: String!) {adminProfileCreate(data: {name: $name '
                     'surname: $surname organizationID: $organizationID login: $login email: $email phone: $phone}) {'
                     'user { id registeredAt status login phone email}}}',
        }
        result = post_request(create_user_query, token)
        return result
    except (ConnectionError, NameError):
        return False


def update_user(user_id_value: str,
                name: str,
                surname: str,
                login: str,
                email: str,
                phone: str,
                organization_id: str,
                token: str) -> dict | bool:
    """
    Редактирование пользователя
        Args:
            user_id_value: уникальный номер уже существующего пользователя
            name: имя пользователя
            surname: фамилия пользователя
            organization_id: уникальный номер организации
            login: логин пользователя
            email: почта пользователя
            phone: телефон пользователя
            token: токен авторизации
        Returns:
            Возвращает словарь с данными по профилю отредактированного пользователя
    """
    try:
        update_user_query = {
            'operationName': 'adminProfileUpdate',
            'variables': {
                'input': {
                    'name': f'{name}',
                    'surname': f'{surname}',
                    'login': f'{login}',
                    'email': f'{email}',
                    'phone': f'{phone}',
                    'organizationID': f'{organization_id}',
                },
                'id': f'{user_id_value}',
            },
            'query': 'mutation adminProfileUpdate($input: AdminProfileData!, $id: ID!)'
            '{adminProfileUpdate(id: $id, data: $input)'
            ' {user {id email}, person {name, surname}, roles {name, code}, '
            'organization {id, shortName} }}',
        }
        result = post_request(update_user_query, token)
        return result
    except (ConnectionError, NameError):
        return False


def block_user(user_id_value: str,
               token: str) -> dict | bool:
    """
    Блокирование пользователя
        Args:
            user_id_value: уникальный номер пользователя
            token: токен авторизации
        Returns:
            Показывается статус блокировки
    """
    try:
        block_user_query = {
            'operationName': 'adminProfileBlock',
            'variables': {'id': f'{user_id_value}'},
            'query': 'mutation adminProfileBlock($id: ID!) {'
            'adminProfileBlock(id: $id){  user{ id blockedAt}}}',
        }
        result = post_request(block_user_query, token)
        return result
    except (ConnectionError, NameError):
        return False


def activate_user(user_id_value: str,
                  token: str) -> dict | bool:
    """
    Активация пользователя
        Args:
            user_id_value: уникальный номер пользователя
            token: токен авторизации
        Returns:
            Показывается статус блокировки
    """
    try:
        activate_user_query = {
            'operationName': 'AdminProfileActivate',
            'variables': {'id': f'{user_id_value}'},
            'query': 'mutation adminProfileActivate($id: ID!) '
            '{adminProfileActivate(id: $id){  user{ id activatedAt}}}',
        }
        result = post_request(activate_user_query, token)
        return result
    except (ConnectionError, NameError):
        return False


def get_count_of_users(token: str) -> int:
    """Получить количество записей
    Args:
        token: токен доступа
    Returns:
        Возвращается количество записей
    """
    get_users_query = {
        'query': 'query adminProfiles{ adminProfiles { user { id login } } }'
    }
    rows = post_request(get_users_query, token)['data']['adminProfiles']
    return len(rows)
