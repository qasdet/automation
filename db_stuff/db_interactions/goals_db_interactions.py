from db_stuff.sqlalchmy_interactions import establish_postgresql_connection
from db_stuff.models.db_models import Goals


def get_goal_id_by_code(goal_code: str) -> Goals:
    """Получить id правила по коду
    Args:
        goal_code: код правила
    Returns:
        id правила
    """
    session = establish_postgresql_connection()
    row = session.query(Goals.id).filter(Goals.code == goal_code).first()
    session.close()
    return row[0]
