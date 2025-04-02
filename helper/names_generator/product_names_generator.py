from faker import Faker


def product_data_generator(
    client_id: str,
    brand_id: str,
    category_id: str = 'bf5e67e6-5849-4e7f-84b5-21d3d175c4bb',
    type_id: str = '2a0f623a-f8a9-4af0-afdb-633956553e83',
) -> dict:
    """Создаётся словарь из шести записей, необходимых для дальнейшей отправки на сервер, чтобы создать
    новый продукт

    Args:
        client_id: Идентификатор созданного клиента
        brand_id: Идентификатор созданного бренда
        category_id: Идентификатор категории продукта. Категории продукта уже созданы,
                    поэтому можно брать любой существующий
        type_id: Идентификатор типа продукта. Типы продукта уже созданы, поэтому можно брать любой существующий.

    Returns:
        Возвращает словарь, который содержит информацию необходимую для отправки на сервер
    """
    product_data = {
        'name': Faker().word('noun').capitalize() + '-prod',
        'naming': Faker().company()[:6]
        + '-'
        + str(Faker().random.randint(1, 200)),
        'client_id': client_id,
        'brand_id': brand_id,
        'category_id': category_id,
        'type_id': type_id,
    }
    return product_data
