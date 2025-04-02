from db_stuff.sqlalchmy_interactions import establish_postgresql_connection
from db_stuff.models.db_models import Clients


def get_clients_db() -> list | bool:
    """Получить список клиентов из БД"""
    session = establish_postgresql_connection()
    row = session.query(Clients).all()
    session.close()
    output_list = []
    if len(row) <= 0:
        return False
    else:
        for each_record in row:
            result = {
                'id': str(each_record.id),
                'name': each_record.name,
                'naming': each_record.naming,
                'full_name': each_record.full_name,
                'inn': each_record.inn,
                'kpp': each_record.kpp,
                'acl_organization_id': str(each_record.acl_organization_id),
            }
            output_list.append(result)
        return output_list


def get_client_by_naming(naming: str) -> dict:
    """Получить клиента из БД по неймингу
    Args:
        naming: нейминг
    Returns:
        Клиент
    """
    session = establish_postgresql_connection()
    row = session.query(Clients).filter(Clients.naming == naming).first()
    session.close()
    return row


def get_client_id_by_naming(client_naming: str) -> str:
    """Получить id клиента из БД по неймингу
    Args:
        client_naming: нейминг клиента
    Returns:
        id клиента
    """
    session = establish_postgresql_connection()
    row = session.query(Clients.id).filter(Clients.naming == client_naming).first()
    session.close()
    if row[0] != '':
        return row[0]
    else:
        return ''


def get_clients_data_by_organization_id(organization_id_value: str) -> list:
    """Получить данные клиентов для справочников из таблицы brands по уникальному номеру организации
        Args:
            organization_id_value: уникальный номер организации
        Returns:
            Данные клиентов для справочников(списки из списков внутри списка)
    """
    session = establish_postgresql_connection()
    clients_data = (
        session.query(Clients.naming, Clients.name)
        .filter(Clients.acl_organization_id == organization_id_value)
        .order_by(Clients.name)
        .all()
    )
    # делим выборку на списки с маскимальной вместительностью 10 шт, как на странице справочника
    result = [clients_data[i:i + 10] for i in range(0, len(clients_data), 10)]
    return list(result)


def delete_client_by_id(client_id: int) -> None:
    """Удалить клиента по id
    Args:
        client_id id организации
    """
    session = establish_postgresql_connection()
    session.query(Clients).filter(Clients.id == client_id).delete()
    session.commit()
    session.close()
