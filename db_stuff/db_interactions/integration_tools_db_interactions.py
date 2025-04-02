from db_stuff.sqlalchmy_interactions import establish_postgresql_connection
from db_stuff.models.db_models import IntegrationTools


def get_tool_id_by_code(integration_tool_code: str) -> IntegrationTools:
    """Получить id инструмента интеграции по коду
    Args:
        integration_tool_code: код инструмента интеграции
    Returns:
        id инструмента интеграции
    """
    session = establish_postgresql_connection()
    row = session.query(IntegrationTools.id).filter(IntegrationTools.code == integration_tool_code).first()
    session.close()
    return row[0]
