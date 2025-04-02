import pytest
import requests

from gitlab_conf import ENV_VARIABLES


def post_request(query: dict, token: str, with_errors: bool = False) -> dict:
    """Выполнение post-запроса

    Args:
        query: Тело запроса
        token: токен доступа ( Например: {"authorization": "Bearer ...some_token..."} )
        with_errors: False - проверять, что запрос выполнен без ошибок,
                               True - Проверяем, что запрос выполнен с ошибками
    """
    try:
        response = requests.post(
            ENV_VARIABLES.get(str('graphql_url')),
            json=query,
            verify=False,
            headers=token,
        )
        if with_errors:
            assert (
                response.json().get('errors') is not None
            ), 'Запрос выполнен без ошибок'
        else:
            assert (
                response.status_code == 200
            ), f'Код ответа не 200. {response.text}'
            assert (
                response.json().get('errors') is None
            ), f"Запрос выполнен с ошибками {response.json().get('errors')}"
        return response.json()
    except ConnectionError:
        pytest.fail('Backend недоступен')
