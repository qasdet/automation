from faker import Faker
from http_methods.post import post_request

fake = Faker()


def strat_plan_delete(strat_plan_id: str, user_office_token: str) -> bool:
    """Отправка запроса на сервер для удаления страт-плана
    Args:
        strat_plan_id: идентификатор страт-плана, который необходимо удалить
        user_office_token: токен авторизации в user-office

    Returns:
        Удаляет страт-план через graphql-запрос и возвращает булево значение об успехе/неуспехе.
    """
    strat_plan_deletion_query = {
        'operation_name': 'stratPlanDelete',
        'variables': {'id': f'{strat_plan_id}'},
        'query': 'mutation stratPlanDelete($id: ID!) {stratPlanDelete(id: $id)}',
    }
    result = post_request(strat_plan_deletion_query, user_office_token)
    return result['data']


def get_strat_plans(user_office_token: str) -> dict:
    """Отправка запроса на сервер для удаления страт-плана
    Args:
        user_office_token: токен авторизации в user-office

    Returns:
        Удаляет страт-план через graphql-запрос и возвращает булево значение об успехе/неуспехе.
    """
    strat_plans_query = {
        'operation_name': 'stratPlans',
        'query': 'query {stratPlans {id}}',
    }
    result = post_request(strat_plans_query, user_office_token)
    return result['data']
