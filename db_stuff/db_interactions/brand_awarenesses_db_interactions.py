from db_stuff.sqlalchmy_interactions import establish_postgresql_connection
from db_stuff.models.db_models import BrandAwarenesses


def get_brand_awareness_name_by_id(brand_awareness_id: str) -> str | bool:
    """Получить название известности бренда по id
    Args:
        brand_awareness_id: id известности бренда
    Returns:
        название известности бренда
    """
    session = establish_postgresql_connection()
    result = session.query(BrandAwarenesses.name).filter(BrandAwarenesses.id == brand_awareness_id).first()
    session.close()
    if result != '':
        return result[0]
    else:
        return False
