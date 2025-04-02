from db_stuff.sqlalchmy_interactions import establish_postgresql_connection
from db_stuff.models.db_models import Departments


def check_departments_record(naming_d: str):
    """Запрос на проверку наличия департамента в бд"""
    session = establish_postgresql_connection()
    q = session.query(Departments).filter_by(name=naming_d)
    return q.first()


def create_departments_record(name_d: str, naming_d: str, code_d: str, acl_organization_id_d: str):
    """Если департамента нет, то департамент создается"""
    session = establish_postgresql_connection()
    validation_brands = Departments(
        name=name_d,
        naming=naming_d,
        code=code_d,
        acl_organization_id=acl_organization_id_d,
    )
    session.add(validation_brands)
    session.commit()
    session.close()


def delete_departments_record(naming_d: str):
    """Удаление записи департамента из бд"""
    session = establish_postgresql_connection()
    session.query(Departments).filter_by(naming=naming_d).delete()
    session.commit()
    session.close()
