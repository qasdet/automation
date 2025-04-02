from db_stuff.sqlalchmy_interactions import establish_postgresql_connection
from db_stuff.models.db_models import ProductPriceCategories


def get_list_of_the_product_price_categories_from_db(without_id: bool = False):
    """Получение всех записей из БД
    Returns:
        список записей
    """
    session = establish_postgresql_connection()
    rows = (
        session.query(ProductPriceCategories)
        .order_by(ProductPriceCategories.id)
        .all()
    )
    session.close()
    if without_id:
        return [{'name': row.name, 'code': row.code} for row in rows]
    return [
        {
            'id': str(row.id),
            'name': row.name,
            'code': row.code,
        }
        for row in rows
    ]
