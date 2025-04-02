from http_methods.post import post_request


def get_admin_instruments(token: str, source_filter: str) -> dict:
    """Получить все верификаторы
    Args:
        token: токен доступа
        source_filter: значение, по которому будет формировать выборка инструментов (TRACKER, VERIFICATOR, POSTCLICK)
    Returns:
        Словарь с площадками, каждая запись содержит в себе: id name naming code url status
    """
    get_admin_sources_query = {
        "operation_name": "adminSources",
        "variables": {"filter": {"type": [f"{source_filter}"]}},
        "query": "query adminSources($filter: SourceFilter) {adminSources(filter: $filter) { id name code url }}"
    }
    rows = post_request(get_admin_sources_query, token)['data']['adminSources']
    return rows
