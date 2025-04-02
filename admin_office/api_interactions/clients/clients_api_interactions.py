from faker import Faker
from http_methods.post import post_request

fake = Faker()


def create_client_user_office(
        client_data: dict, user_office_token: str
) -> str:
    """Отправка запроса на сервер для создания нового клиента через user-office
    Args:
        client_data: созданный словарь, который содержит данные, необходимые для заполнения обя-
        зательных полей: name, naming
        user_office_token: токен авторизации в user-office

    Returns:
        Создаёт клиента через graphql-запрос и возвращает id только что созданного клиента.
    """
    client_creation_query = {
        'operation_name': 'ClientCreate',
        'variables': {
            'data': {
                'name': client_data['name'],
                'naming': client_data['naming'],
            }
        },
        'query': """mutation ClientCreate($data: ClientData!) {
                          clientCreate(data: $data) {id}}""",
    }
    result = post_request(client_creation_query, user_office_token)
    return result['data']['clientCreate']['id']


def create_client_admin_office(name: str,
                               naming: str,
                               full_name: str,
                               inn: str,
                               kpp: str,
                               organization_id: str,
                               admin_office_token: str) -> dict:
    """Отправка запроса на сервер для создания нового клиента через admin-office с правами администратора
    Args:
        name: имя создаваемого клиента
        naming: нейминг создаваемого клиента
        full_name: полное имя создаваемого клиента
        inn: инн создаваемого клиента
        kpp: кпп создаваемого клиента
        organization_id: уникальный номер организации
        admin_office_token: токен авторизации в admin-office

    Returns:
        Создаёт клиента через graphql-запрос с правами администратора и возвращает id только что созданного клиента.
    """
    create_client_query = {
        'variables': {'name': f'{name}',
                      'naming': f'{naming}',
                      'fullName': f'{full_name}',
                      'inn': f'{inn}',
                      'kpp': f'{kpp}',
                      'organizationID': f'{organization_id}'},
        'query': 'mutation ($name: String! $naming: String!'
                 ' $fullName: String $inn: String $kpp: String $organizationID: ID!) '
                 '{adminClientCreate(data:{name: $name naming: $naming fullName: $fullName inn: $inn'
                 ' kpp: $kpp organizationID: $organizationID }) '
                 '{id name naming fullName inn kpp organization {id}}}',
    }
    result = post_request(create_client_query, admin_office_token)
    return result['data']['adminClientCreate']


def get_clients_api(token):
    """ Получить список клиентов в Admin Office с правами администратора
    Args:
        token: токен, для авторизации на сервер
    Returns:
        Словарь, содержащий список клиентов
    """
    get_clients_query = {
        'operation_name': 'adminClients',
        'variables': {},
        'query': 'query {adminClients {id name naming code fullName inn kpp organization {id}}}',
    }
    result = post_request(get_clients_query, token)['data']['adminClients']
    return result


def get_client_info(id_value: str, token: str) -> str | bool:
    """ Получить информацию по одному клиенту в Admin Office с правами администратора
    Args:
        id_value: уникальный номер определённого клиента
        token: токен, для авторизации на сервер
    Returns:
        Словарь, содержащий данные по одному клиенту
    """
    get_client_info_query = {
        'operation_name': 'adminClients',
        'variables': f"{id_value}",
        'query': 'query($id: ID!) {adminClients(id: $id) {id name naming code fullName inn kpp organization {id}}}',
    }
    try:
        result = post_request(get_client_info_query, token)['data']['adminClients']
        return result
    except AssertionError:
        return True


def update_client(id_value: str,
                  name: str,
                  naming: str,
                  full_name: str,
                  inn: str,
                  kpp: str,
                  admin_office_token: str) -> dict:
    """ Обновление данных с правами администратора
    Args:
        id_value: уникальный номер клиента
        name: имя создаваемого клиента
        naming: нейминг клиента
        full_name: полное имя клиента
        inn: инн клиента
        kpp: кпп клиента
        admin_office_token: токен авторизации в admin-office
    Returns:
        Словарь, содержащий обновлённые данные по одному клиенту
    """
    update_client_query = {
        'variables': {'id': f'{id_value}',
                      'data': {'name': f'{name}',
                               "naming": f'{naming}',
                               "fullName": f'{full_name}',
                               "inn": f'{inn}',
                               "kpp": f'{kpp}'}},
        'query': 'mutation adminClientUpdate($id: ID! $data: ClientData!)'
                 ' {adminClientUpdate (id: $id data: $data) {id name naming fullName inn kpp}}',
    }
    result = post_request(update_client_query, admin_office_token)
    return result['data']['adminClientUpdate']


def delete_client_by_id(id_client: str, token: str) -> dict | bool:
    """Удаление клиента с правами администратора

    Args:
        id_client: id клиента
        token: токен доступа
    """
    query = {
        'operationName': 'adminClientDelete',
        'variables': {'id': f'{id_client}'},
        'query': 'mutation adminClientDelete($id: ID!) {adminClientDelete(id: $id)}',
    }
    response = post_request(query, token)
    if response:
        return response
    else:
        return False
