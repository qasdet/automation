from db_stuff.sqlalchmy_interactions import establish_postgresql_connection
from db_stuff.models.db_models import Departments


def get_department_id_by_naming(naming: str) -> Departments:
    """Получить id подразделения из БД по неймингу
    Args:
        naming: нейминг
    Returns:
        id подразделения
    """
    session = establish_postgresql_connection()
    row = session.query(Departments.id).filter(Departments.naming == naming).first()
    session.close()
    return row[0]
