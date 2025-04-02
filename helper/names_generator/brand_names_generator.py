from faker import Faker


def brand_data_generator(client_id: str) -> dict:
    """Создаётся словарь из трёх записей, необходимых для дальнейшей отправки на сервер, чтобы создать
    новый бренд. Один ключ выступает в качестве аргумента

    Args:
        client_id: Нужен для корректной привязки бренда к
    продукту. Без этого параметра невозможно создать новый бренд.

    Returns:
        Возвращает словарь, который содержит
    информацию необходимую для отправки на сервер.
    """
    brand_data = {
        'name': Faker().word('noun').capitalize() + '-brand',
        'naming': Faker().word('noun')[:6]
        + '-'
        + str(Faker().random.randint(1, 200)),
        'client_id': client_id,
    }
    return brand_data
