from db_stuff.sqlalchmy_interactions import establish_postgresql_connection
from db_stuff.models.db_models import BuyTypes


def get_buy_type_id_by_naming(buy_type_naming: str) -> BuyTypes:
    """Получить id типа закупки по неймингу
    Args:
        buy_type_naming: нейминг типа закупки
    Returns:
        id типа закупки
    """
    session = establish_postgresql_connection()
    row = session.query(BuyTypes.id).filter(BuyTypes.naming == buy_type_naming).first()
    session.close()
    return row[0]


def get_buy_type_name_by_id(buy_type_id: str) -> str | bool:
    """Получить название типа закупки по id
    Args:
        buy_type_id: id типа закупки
    Returns:
        название типа закупки
    """
    session = establish_postgresql_connection()
    result = session.query(BuyTypes.name).filter(BuyTypes.id == buy_type_id).first()
    session.close()
    if result != '':
        return result[0]
    else:
        return False
