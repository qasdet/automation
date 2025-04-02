import requests

from datetime import datetime
from faker import Faker
from http_methods.post import post_request
from gitlab_conf import ENV_VARIABLES

fake = Faker('ru_RU')


fake = Faker()


def get_user_candidate_data(admin_office_token: str, id_value: list) -> dict:
    """Отправка запроса на сервер для получения словаря, который содержит данные по заявке пользователя
    Args:
        admin_office_token: токен авторизации в admin-office
        id_value: уникальный номер заявки
    Returns:
        Словарь с данными из заявки
    """
    get_specific_user_candidate_query = {
        "operation_name": "adminCandidates",
        "variables": {"id": f"{id_value}"},
        "query": "query adminCandidates($id: ID!) {adminCandidates(id: $id) {"
                 "id name surname email phone firmName comments}}",
    }
    result = post_request(get_specific_user_candidate_query, admin_office_token)
    return result['data']['adminCandidates'][0]


def delete_user_candidate(
        admin_office_token: str, user_candidate_id: str
) -> bool:
    """Отправка запроса на сервер для удаления заявки с лэндинга
    Args:
        admin_office_token: токен авторизации в admin-office
        user_candidate_id: идентификатор заявки
    Returns:
        Булево значение, в зависимости от результата операции
    """
    delete_user_candidate_query = {
        'operation_name': 'userCandidates',
        'variables': {'id': f'{user_candidate_id}'},
        'query': 'mutation adminCandidateDelete($id: ID!) {adminCandidateDelete(id: $id)}',
    }
    result = post_request(delete_user_candidate_query, admin_office_token)
    return result['data']['adminCandidateDelete']


def get_list_of_the_user_candidates(
    token: str, variables: dict = None
) -> list:
    """Запрос на получение записей от сервиса

    Args:
        token: токен доступа
        variables: аргументы запроса
    Returns:
        список записей
    """
    query = {
        'variables': variables if variables is not None else {},
        'query': """query adminCandidates($id: ID, $slice: UserOfficeSlice) {
                        adminCandidates(id: $id, slice: $slice) {
                        id
                        name
                        surname
                        email
                        firmName
                        phone
                        role
                        comments
                        isPerformed
                        createdAt
                        updatedAt
                        }
                    }
            """,
    }
    rows = post_request(query, token)['data']['adminCandidates']
    return [
        {
            'id': row['id'],
            'name': row['name'],
            'surname': row['surname'],
            'email': row['email'],
            'phone': row['phone'],
            'firmName': row['firmName'],
            'role': row['role'],
            "isPerformed": row["isPerformed"],
            'created_at': datetime.strptime(
                row['createdAt'], '%Y-%m-%dT%H:%M:%S.%f%z'
            ).strftime('%Y-%m-%d %H:%M:%S'),
        }
        for row in rows
    ]


def leave_a_request_for_create_user(
    name: str,
    surname: str,
    firm_name: str,
    email: str,
    phone: str,
    role: str,
    comments: str = None,
) -> dict:
    """Оставить заявку
    Args:
        name: Имя
        surname: Фамилия
        firm_name: Название организации
        email: Почта
        phone: Телефон
        role: Роль организации
        comments: Комментарий
    Return:
        Ответ от сервиса (словарь данных)
    """
    payload = {
        'name': name,
        'surname': surname,
        'firm_name': firm_name,
        'email': email,
        'phone': phone,
        'comments': comments,
        'role': role,
    }
    created_at = datetime.now().strftime('%Y-%m-%dT%H:%M')
    response = requests.post(
        url=ENV_VARIABLES['candidate_api_url'],
        json=payload,
        verify=False,
    )
    assert response.status_code == 200, (
        f'Запрос выполнен с ошибкой. '
        f'Код ответа = {response.status_code}. Ошибка {response.text}'
    )
    payload.update(
        {
            'created_at': created_at,
            'deleted_at': None,
            'id': response.json()['id'],
        }
    )
    return payload


def delete_user_candidate_by_id(id_user_candidate: int, token: str) -> None:
    """Удаление заявки

    Args:
        id_user_candidate: id заявки
        token: токен доступа
    """
    query = {
        'operationName': 'adminCandidateDelete',
        'variables': {'id': f'{id_user_candidate}'},
        'query': 'mutation adminCandidateDelete($id: ID!) {\n  adminCandidateDelete(id: $id)\n}',
    }

    response = post_request(query, token)
    assert response == {
        'data': {'adminCandidateDelete': True}
    }, 'Заявка удалена'
