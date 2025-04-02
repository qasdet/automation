from http_methods.post import post_request


def get_list_of_the_ad_sizes(token: str, variables: dict = None) -> list:
    """Запрос на получение записей от сервиса

    Args:
        token: токен доступа
        variables: аргументы запроса
    Returns:
        список записей
    """
    query = {
        'variables': variables if variables is not None else {},
        'query': """query AdminAdSizes($id: ID, $filter: AdSizeFilter, $slice: UserOfficeSlice) {
                  adminAdSizes(id: $id, filter: $filter, slice: $slice) {
                    ...AdSize
                    __typename
                  }
                }

                fragment AdSize on AdSize {
                  id
                  name
                  code
                  __typename
                }
            """,
    }
    rows = post_request(query, token)['data']['adminAdSizes']
    return [
        {'id': str(row['id']), 'name': row['name'], 'code': row['code']}
        for row in rows
    ]
