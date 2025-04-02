from db_stuff.sqlalchmy_interactions import establish_postgresql_connection
from db_stuff.models.db_models import Sources


def get_source_id_by_naming(source_naming: str) -> Sources | bool:
    """Получить id площадки по неймингу
    Args:
        source_naming: нейминг площадки
    Returns:
        id площадки
    """
    session = establish_postgresql_connection()
    row = session.query(Sources.id).filter(Sources.naming == source_naming).first()
    session.close()
    if row is None:
        return False
    else:
        return row[0]


def get_source_name_by_id(source_id: str) -> str | bool:
    """Получить название площадки по id
    Args:
        source_id: id площадки
    Returns:
        название площадки
    """
    session = establish_postgresql_connection()
    result = session.query(Sources.name).filter(Sources.id == source_id).first()
    session.close()
    if result != '':
        return result[0]
    else:
        return False


def delete_source_by_id(source_id: str) -> None:
    """Удалить площадку по id
    Args:
        source_id: id площадки
    Returns:
    """
    session = establish_postgresql_connection()
    session.query(Sources).filter(Sources.id == source_id).delete()
    session.commit()
    session.close()
