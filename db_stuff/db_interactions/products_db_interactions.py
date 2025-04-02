from typing import Any

from db_stuff.sqlalchmy_interactions import establish_postgresql_connection
from db_stuff.models.db_models import Products, ProductTypes


def get_product_by_naming(naming: str) -> Products:
    """Получить продукт из БД по неймингу
    Args:
        naming: нейминг
    Returns:
        Продукт
    """
    session = establish_postgresql_connection()
    row = session.query(Products).filter(Products.naming == naming).first()
    session.close()
    return row


def get_product_id_by_naming(naming: str) -> bool | str:
    """Получить id продукта из БД по неймингу
    Args:
        naming: нейминг
    Returns:
        id продукта
    """
    session = establish_postgresql_connection()
    row = session.query(Products.id).filter(Products.naming == naming).first()
    session.close()
    if row is None:
        return False
    else:
        return str(row[0])


def get_product_name_by_id(product_id: str) -> Products:
    """Получить наименование продукта из БД по id
    Args:
        product_id: id продукта
    Returns:
        наименование продукта
    """
    session = establish_postgresql_connection()
    row = session.query(Products.name).filter(Products.id == product_id).first()
    session.close()
    return row[0]


def get_products_data_by_organization_id(organization_id_value: str) -> list:
    """Получить данные продуктов для справочников из таблицы products по уникальному номеру организации
        Args:
            organization_id_value: уникальный номер организации
        Returns:
            Данные продуктов для справочников(списки из списков внутри списка)
    """
    session = establish_postgresql_connection()
    products_dict_data = (
        session.query(Products.name, Products.naming, ProductTypes.name)
        .outerjoin(ProductTypes, Products.type_id == ProductTypes.id)
        .filter(
            (Products.acl_organization_id == organization_id_value) and
            ((ProductTypes.id == Products.type_id) | (ProductTypes.id.is_(None)))
        )
        .order_by(Products.name)
        .all()
    )
    # заменяем None на "-"
    formatted_products_dict_data = [
        list("-" if x is None else x for x in row)
        for row in products_dict_data
    ]
    # делим выборку на списки с маскимальной вместительностью 10 шт, как на странице справочника
    result = [formatted_products_dict_data[i:i + 10] for i in range(0, len(formatted_products_dict_data), 10)]
    return result
