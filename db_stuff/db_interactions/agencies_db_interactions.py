from db_stuff.sqlalchmy_interactions import establish_postgresql_connection
from db_stuff.models.db_models import Agencies


def get_agency_id_by_naming(naming: str) -> Agencies:
    """Получить id агентства из БД по неймингу
    Args:
        naming: нейминг
    Returns:
        id агентства
    """
    session = establish_postgresql_connection()
    row = session.query(Agencies.id).filter(Agencies.naming == naming).first()
    session.close()
    return row[0]
