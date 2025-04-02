from http_methods.post import post_request


def get_list_of_product_price_categories(token: str) -> list:
    """Запрос на получение записей от сервиса
    Returns:
        список записей
    """
    admin_product_price_categories_query = {
        "variables": {},
        "query": "query adminProductPriceCategories {adminProductPriceCategories {id name code}}",
    }
    rows = post_request(admin_product_price_categories_query, token)['data']['adminProductPriceCategories']
    return rows
