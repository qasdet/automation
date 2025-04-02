from faker import Faker
from http_methods.post import post_request

fake = Faker()


def create_product_user_office(
        product_data: dict, user_office_token: str
) -> str:
    """Отправка запроса на сервер для создания нового продукта
    Args:
        product_data: созданный словарь, который содержит данные, необходимые для заполнения
        обязательных полей: name, naming, id клиента, id бренда, id категории и id типа продукта
        user_office_token: токен авторизации в user-office

    Returns:
        Создаёт продукт через graphql-запрос и возвращает уникальный номер только что созданного продукта.
    """
    product_creation_query = {
        'operation_name': 'productCreate',
        'variables': {
            'data': {
                'name': product_data['name'],
                'naming': product_data['naming'],
                'categoryID': product_data['product_category_id'],
                'typeID': product_data['product_type_id'],
            }
        },
        'query': """mutation ProductCreate($data: ProductData!) {
                    productCreate(data: $data) {id}}""",
    }
    result = post_request(product_creation_query, user_office_token)
    return result['data']['productCreate']['id']


def delete_product_by_id(id_product: str, token: str) -> None:
    """Удаление продукта по id

    Args:
        id_product: id продукта
        token: токен доступа
    """
    query = {
        'operationName': 'adminProductDelete',
        'variables': {'id': f'{id_product}'},
        'query': 'mutation adminProductDelete($id: ID!) {adminProductDelete(id: $id)}',
    }

    response = post_request(query, token)
    assert response == {
        'data': {'adminProductDelete': True}
    }, 'Продукт не удалён'


def get_count_of_products(token: str) -> list:
    """Получить количество записей
    Args:
        token: токен доступа
    Returns:
        Возвращается количество записей
    """
    get_product_list_query = {
        "operation_name": "adminProducts",
        "query": "query adminProducts {adminProducts {id name}}"
    }
    rows = post_request(get_product_list_query, token)['data']['adminProducts']
    return rows
