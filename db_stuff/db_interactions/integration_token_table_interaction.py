from db_stuff.sqlalchmy_interactions import establish_postgresql_connection
from db_stuff.models.db_models import IntegrationTokens


def get_integration_token_id(account: str) -> bool | str:
    """Проверить, есть ли запись в базе по source_account
    Args:
        account: имя подключенного аккаунта
    Returns:
        True or integration_token_id
    """
    session = establish_postgresql_connection()
    row = session.query(IntegrationTokens.id).filter(IntegrationTokens.account.ilike(
        f"%{account}%"))
    result = row.first()
    session.close()
    if result is None:
        return False
    else:
        return str(result[0])


def get_source_account_by_integration_token(integration_token_id_value: str) -> bool | str:
    """Найти запись в таблице integration_tokens по id
    Args:
        integration_token_id_value:
    Returns:
        Находит запись по айди
    """
    session = establish_postgresql_connection()
    row = session.query(IntegrationTokens.source_account).filter(
        IntegrationTokens.id == integration_token_id_value)
    session.close()
    result = row.first()
    if result is None:
        return False
    else:
        return str(result[0])


# TODO: Добавить вменяемый вывод, чтобы было понятно, что вообще произошло и с каким результатом.
def delete_integration_token_record_by_id(integration_token_record_id: str) -> bool:
    """Получив на вход id записи интеграционного токена, выполнить удаление. Вернуть флаг Истина, если удаление успешное
    Args:
        integration_token_record_id: id подключенного аккаунта
    Returns:
        True or False
    """
    session = establish_postgresql_connection()
    row = session.query(IntegrationTokens).filter_by(id=integration_token_record_id).delete()
    print(row)
    session.commit()
    session.close()
