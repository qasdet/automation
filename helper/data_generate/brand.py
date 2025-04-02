from db_stuff.sqlalchmy_interactions import establish_postgresql_connection
from db_stuff.models.db_models import Brands


def check_brand_record(naming_b: str):
    """Запрос на проверку наличия бренда в бд"""
    session = establish_postgresql_connection()
    q = session.query(Brands).filter_by(name=naming_b)
    return q.first()


def create_brand_record(name_b: str, naming_b: str, code_b: str, awareness_id_b: str, acl_organization_id_b: str):
    """Если бренда нет, то бренда создается"""
    session = establish_postgresql_connection()
    validation_brands = Brands(
        name=name_b,
        naming=naming_b,
        code=code_b,
        awareness_id=awareness_id_b,
        acl_organization_id=acl_organization_id_b,
    )
    session.add(validation_brands)
    session.commit()
    session.close()


def delete_brand_record(naming_b: str):
    """Удаление записи бренда из бд"""
    session = establish_postgresql_connection()
    session.query(Brands).filter_by(name=naming_b).delete()
    session.commit()
    session.close()
