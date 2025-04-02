from http_methods.post import post_request


def get_admin_sources(token: str) -> dict:
    """Получить все площадки
    Args:
        token: токен доступа
    Returns:
        Словарь с площадками, каждая запись содержит в себе: id name naming code url status
    """
    get_admin_sources_query = {
        "operation_name": "adminSources",
        "variables": {},
        "query": "query adminSources {adminSources { id name naming code url status}}"
    }
    rows = post_request(get_admin_sources_query, token)['data']['adminSources']
    return rows


def get_specific_source_by_id(source_id: str, token: str) -> dict:
    """Получить данные площадки
    Args:
        source_id: уникальный номер площадки
        token: токен доступа
    Returns:
        Словарь площадки: id name naming code url status
    """
    get_admin_sources_query = {
        "operation_name": "adminSources",
        "variables": {'id': f"{source_id}"},
        "query": "query adminSources($id: ID!) {adminSources(id: $id) { id name naming code url status}}"
    }
    result = post_request(get_admin_sources_query, token)['data']['adminSources']
    return result
