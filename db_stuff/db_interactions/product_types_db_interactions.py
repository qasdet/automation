from db_stuff.sqlalchmy_interactions import establish_postgresql_connection
from db_stuff.models.db_models import ProductTypes


def get_product_type_id_by_code(product_type_code: str) -> str:
    """Получить id типа продукта из БД по коду
    Args:
        product_type_code: код типа продукта
    Returns:
        id типа продукта
    """
    session = establish_postgresql_connection()
    row = session.query(ProductTypes.id).filter(ProductTypes.code == product_type_code).first()
    session.close()
    if row != '':
        return row[0]
    else:
        return ''
