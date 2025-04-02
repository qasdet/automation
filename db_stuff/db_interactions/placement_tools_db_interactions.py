from db_stuff.sqlalchmy_interactions import establish_postgresql_connection
from db_stuff.models.db_models import PlacementTools


def check_placement_tools_specific_record(integration_token_record_id: str) -> bool | dict:
    """Найти запись в таблице placement_tools по integration_token_id
    Args:
        integration_token_record_id:
    Returns:
        Находит запись по айди
    """
    session = establish_postgresql_connection()
    row = session.query(PlacementTools.id, PlacementTools.tool_type).filter(
        PlacementTools.integration_token_id == integration_token_record_id)
    session.close()
    result = row.first()
    if result is None:
        return False
    else:
        dict_result = {'id': str(result[0]), 'tool_type': str(result[1])}
        return dict_result


def delete_placement_tool_record_by_id_and_tool_type(integration_token_record_id: str, tool_type_value: str) -> bool:
    """Получив на вход id записи интеграционного токена, выполнить удаление. Вернуть флаг Истина, если удаление успешное
    Args:
        integration_token_record_id: id подключенного аккаунта
        tool_type_value: тип подключения
    Returns:
        True or False
    """
    session = establish_postgresql_connection()
    row = session.query(PlacementTools).filter_by(id=integration_token_record_id, tool_type=tool_type_value).delete()
    print(row)
    session.commit()
    session.close()
