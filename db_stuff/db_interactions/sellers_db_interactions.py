from db_stuff.sqlalchmy_interactions import establish_postgresql_connection
from db_stuff.models.db_models import Sellers


def get_seller_id_by_naming(seller_naming: str) -> Sellers:
    """Получить id продавца по неймингу
    Args:
        seller_naming: нейминг продавца
    Returns:
        id продавца
    """
    session = establish_postgresql_connection()
    row = session.query(Sellers.id).filter(Sellers.naming == seller_naming).first()
    session.close()
    return row[0]


def get_seller_name_by_id(seller_id: str) -> str | bool:
    """Получить название продавца по id
    Args:
        seller_id: id продавца
    Returns:
        название продавца
    """
    session = establish_postgresql_connection()
    result = session.query(Sellers.name).filter(Sellers.id == seller_id).first()
    session.close()
    if result != '':
        return result[0]
    else:
        return False
