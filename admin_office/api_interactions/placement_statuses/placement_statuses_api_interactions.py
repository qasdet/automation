from http_methods.post import post_request


def get_list_of_the_placement_statuses(token) -> list:
    """Запрос на получение записей от сервиса
    Returns:
        список записей
    """
    get_list_of_the_placement_statuses_query = {
        "variables": {},
        "query": "query adminPlacementStatuses {adminPlacementStatuses {id name code}}"
    }
    rows = post_request(get_list_of_the_placement_statuses_query, token)['data']['adminPlacementStatuses']
    return rows
