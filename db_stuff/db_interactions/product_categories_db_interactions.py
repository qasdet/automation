from db_stuff.sqlalchmy_interactions import establish_postgresql_connection
from db_stuff.models.db_models import ProductCategories


def get_product_category_id_by_code(product_category_code: str) -> str:
    """Получить id категории продукта из БД по коду
    Args:
        product_category_code: код категории продукта
    Returns:
        id категории продукта
    """
    session = establish_postgresql_connection()
    row = session.query(ProductCategories.id).filter(ProductCategories.code == product_category_code).first()
    session.close()
    if row[0] != '':
        return row[0]
    else:
        return ''
