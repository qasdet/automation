from db_stuff.sqlalchmy_interactions import establish_postgresql_connection
from db_stuff.models.db_models import Agencies


def check_agency_record(name_agency: str):
    """Запрос на проверку наличия Агентства в бд"""
    session = establish_postgresql_connection()
    q = session.query(Agencies).filter_by(name=name_agency)
    return q.first()


def create_agency_record(acl_organizations_id: str, name_agency: str, naming_agency: str, creators_user_id: str):
    """Если агентства нет, то агентство создается"""
    session = establish_postgresql_connection()
    validation_brands = Agencies(
        acl_organization_id=acl_organizations_id,
        name=name_agency,
        naming=naming_agency,
        creator_user_id=creators_user_id
    )
    session.add(validation_brands)
    session.commit()
    session.close()


def delete_agency_record(name_agency: str):
    """Удаление записи агентства из бд"""
    session = establish_postgresql_connection()
    session.query(Agencies).filter_by(name=name_agency).delete()
    session.commit()
    session.close()
