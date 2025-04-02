import string

from faker import Faker

from admin_office.constants import ORGANIZATION

fake = Faker()
BRAND_AWARENESS = 'Высокая'


def brand_name() -> str:
    """Название бренда

    Returns:
        Название бренда
    """
    # Чтобы запись была в первой строке таблицы
    return f"0 {fake.text(5).replace('.', '')}"


def brand_naming() -> str:
    """Нейминг бренда

    Returns:
        Нейминг бренда
    """
    return fake.lexify(text='?' * 4, letters=string.ascii_uppercase)


def make_data_all_brand_fields() -> dict:
    """Данные для всех полей клиента

    Returns:
        Словарь данных
    """

    return {
        'name': brand_name(),
        'naming': brand_naming(),
        'organization': ORGANIZATION,
        'brand_awareness': BRAND_AWARENESS,
    }
