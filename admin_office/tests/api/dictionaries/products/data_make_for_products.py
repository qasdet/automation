import string

from faker import Faker

from admin_office.constants import ORGANIZATION

fake = Faker()
# TODO Заменить на выборку из БД
TYPE_PRODUCT = 'Товар B2C'
PRICE_CATEGORY = 'Премиум'
SEASONALITIES = 'Умеренная'
CATEGORY = 'Корм для животных'
GEOGRAPHIES = 'Местная'
PURCHASE_FREQUENCIES = 'Почти каждый день'
SEASONALITY_VALUES = 'Весна'


def product_name() -> str:
    """Название продукта

    Returns:
        Название продукта
    """
    # Чтобы запись была в первой строке таблицы
    return f"0 {fake.text(5).replace('.', '')}"


def product_naming() -> str:
    """Код продукта

    Returns:
        Код продукта
    """
    return fake.lexify(text='?' * 4, letters=string.ascii_letters)


def make_data_all_product_fields() -> dict:
    """Данные для всех полей продукта

    Returns:
        Словарь данных
    """

    return {
        'name': product_name(),
        'naming': product_naming(),
        'type_product': TYPE_PRODUCT,
        'price_category': PRICE_CATEGORY,
        'seasonalities': SEASONALITIES,
        'category': CATEGORY,
        'geographies': GEOGRAPHIES,
        'purchase_frequencies': PURCHASE_FREQUENCIES,
        'seasonality_values': SEASONALITY_VALUES,
        'organization': ORGANIZATION,
    }
