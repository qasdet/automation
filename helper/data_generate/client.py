from db_stuff.sqlalchmy_interactions import establish_postgresql_connection
from db_stuff.models.db_models import Clients


def check_client_record(naming_c: str):
    """Запрос на проверку наличия клиента в бд"""
    session = establish_postgresql_connection()
    q = session.query(Clients).filter_by(name=naming_c)
    return q.first()


def create_client_record(name_c: str, naming_c: str, code_c: str, acl_organization_id_c: str):
    """Если клиента нет, то клиент создается"""
    session = establish_postgresql_connection()
    validation_brands = Clients(
        name=name_c,
        naming=naming_c,
        code=code_c,
        acl_organization_id=acl_organization_id_c,  # 5b872b04-9bf9-4665-8a6c-9e137fd67066
    )
    session.add(validation_brands)
    session.commit()
    session.close()


def delete_client_record(naming_c):
    """Удаление записи клиента из бд"""
    session = establish_postgresql_connection()
    session.query(Clients).filter_by(name=naming_c).delete()
    session.commit()
    session.close()
