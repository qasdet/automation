from db_stuff.sqlalchmy_interactions import establish_postgresql_connection
from db_stuff.models.db_models import Metrics


def get_metric_name_by_code(metric_code: str) -> str | bool:
    """Получить название метрики из БД по коду
    Args:
        metric_code: код метрики
    Returns:
        название метрики
    """
    session = establish_postgresql_connection()
    result = session.query(Metrics.name).filter(Metrics.code == metric_code).first()
    session.close()
    if result != '':
        return result[0]
    else:
        return False
