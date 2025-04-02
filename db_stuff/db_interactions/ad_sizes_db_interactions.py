from db_stuff.sqlalchmy_interactions import establish_postgresql_connection
from db_stuff.models.db_models import AdSizes


def get_list_of_the_ad_sizes_from_db(without_id: bool = False) -> list:
    """Получение всех записей из БД

    Returns:
        список записей
    """
    session = establish_postgresql_connection()
    rows = session.query(AdSizes).order_by(AdSizes.name).all()
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


def get_row_of_the_ad_sizes_by_id_from_db(ad_size_id: int) -> dict:
    """Получение записи из БД по id
    Args:
        ad_size_id: id записи
    Returns:
        Словарь данных записи
    """
    session = establish_postgresql_connection()
    row = session.query(AdSizes).filter(AdSizes.id == ad_size_id).one()
    session.close()
    return {
        'id': row.id,
        'name': row.name,
        'code': row.code,
        '__typename': 'AdSize',
    }


def get_ad_size_id_by_naming(ad_size_naming: str) -> AdSizes:
    """Получить id размера по неймингу
    Args:
        ad_size_naming: нейминг размера
    Returns:
        id размера
    """
    session = establish_postgresql_connection()
    row = session.query(AdSizes.id).filter(AdSizes.naming == ad_size_naming).first()
    session.close()
    return row[0]


def get_ad_size_name_by_id(ad_size_id: str) -> str | bool:
    """Получить название размера по id
    Args:
        ad_size_id: id размера
    Returns:
        название размера
    """
    session = establish_postgresql_connection()
    result = session.query(AdSizes.name).filter(AdSizes.id == ad_size_id).first()
    session.close()
    if result != '':
        return result[0]
    else:
        return False
