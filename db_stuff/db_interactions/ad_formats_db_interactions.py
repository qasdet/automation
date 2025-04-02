from db_stuff.sqlalchmy_interactions import establish_postgresql_connection
from db_stuff.models.db_models import AdFormats


def get_ad_format_id_by_naming(ad_format_naming: str) -> AdFormats:
    """Получить id формата по неймингу
    Args:
        ad_format_naming: нейминг формата
    Returns:
        id формата
    """
    session = establish_postgresql_connection()
    row = session.query(AdFormats.id).filter(AdFormats.naming == ad_format_naming).first()
    session.close()
    return row[0]


def get_ad_format_name_by_id(ad_format_id: str) -> str | bool:
    """Получить название формата по id
    Args:
        ad_format_id: id формата
    Returns:
        название формата
    """
    session = establish_postgresql_connection()
    result = session.query(AdFormats.name).filter(AdFormats.id == ad_format_id).first()
    session.close()
    if result != '':
        return result[0]
    else:
        return False
