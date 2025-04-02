from faker import Faker


def client_data_generator() -> dict:
    """Создаётся словарь из двух записей, необходимых для дальнейшей отправки на сервер, чтобы создать
    нового клиента"""
    client_data = {
        'name': Faker('ru_RU').company(),
        'naming': Faker('en_US').company()[:6]
        + '-'
        + str(Faker().random.randint(1, 200)),
    }
    return client_data
