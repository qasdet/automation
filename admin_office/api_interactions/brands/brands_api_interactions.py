from http_methods.post import post_request
from faker import Faker

fake = Faker()


def brand_creation(
        brand_data: dict, user_office_token: str
) -> str:
    """Отправка запроса на сервер для создания нового клиента
    Args:
        brand_data: созданный словарь, который содержит данные, необходимые для заполнения обя-
        зательных полей: name, naming, а также id клиента
        user_office_token: токен авторизации в user-office

    Returns:
        Создаёт бренд через graphql-запрос и возвращает id только что созданного бренда.
    """
    brand_creation_query = {
        'operation_name': 'BrandCreate',
        'variables': {
            'data': {
                'name': brand_data['name'],
                'naming': brand_data['naming'],
            }
        },
        'query': """mutation BrandCreate($clientID: ID, $data: BrandData!) {
                     brandCreate(clientID: $clientID, data: $data) {id}}""",
    }
    result = post_request(brand_creation_query, user_office_token)
    return result['data']['brandCreate']['id']


def delete_brand_by_id(id_brand: int, token: str) -> None:
    """Удаление клиента

    Args:
        id_brand: id бренда
        token: токен доступа
    """
    query = {
        'operationName': 'adminBrandDelete',
        'variables': {'id': f'{id_brand}'},
        'query': 'mutation adminBrandDelete($id: ID!) {\n  adminBrandDelete(id: $id)\n}',
    }

    response = post_request(query, token)
    assert response == {'data': {'adminBrandDelete': True}}, 'Клиент не удален'


def get_count_of_brands(token: str) -> int:
    """Получить количество записей
    Args:
        token: токен доступа
    Returns:
        Возвращается количество записей
    """
    get_brands_query = {
        "operationName": "adminBrands",
        "query": "query adminBrands {adminBrands {id name}}",
    }
    rows = post_request(get_brands_query, token)['data']['adminBrands']
    return len(rows)
