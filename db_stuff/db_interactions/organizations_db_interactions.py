from db_stuff.sqlalchmy_interactions import establish_postgresql_connection
from db_stuff.models.db_models import Organizations


def delete_organization_by_id(organization_id: int) -> None:
    """Удалить организацию по id
    Args:
        organization_id: id организации
    """
    session = establish_postgresql_connection()
    session.query(Organizations).filter(
        Organizations.id == organization_id
    ).delete()
    session.commit()
    session.close()


def get_organization_by_inn_and_kpp(inn: str, kpp: str) -> Organizations:
    """Получить организацию из БД по ИНН и КПП
    Args:
        inn: ИНН
        kpp: КПП
    Returns:
        Организация
    """
    session = establish_postgresql_connection()
    row = (
        session.query(Organizations)
        .filter(Organizations.inn == inn and Organizations.kpp == kpp)
        .first()
    )
    session.close()
    return row


def get_organization_by_email(email: str) -> Organizations:
    """Получить организацию из БД по email
    Args:
        email: почтовый ящик
    Returns:
        Организация
    """
    session = establish_postgresql_connection()
    row = (
        session.query(Organizations)
        .filter(Organizations.email == email)
        .first()
    )
    session.close()
    return row


def get_organization_id_by_name(organization_name_value: str) -> str | bool:
    """
    Получить id организации по её названию
        Args:
            organization_name_value: название организации
    Returns:
        Уникальный идентификационный номер организации
    """
    session = establish_postgresql_connection()
    organization_id_value = session.query(
        Organizations.id).filter(Organizations.full_name == organization_name_value).first()
    if organization_id_value:
        return str(organization_id_value[0])
    else:
        return False


def get_organizations_from_db() -> list | bool:
    """
    Получить список организаций
        Args:

    Returns:
        Список организаций
    """
    session = establish_postgresql_connection()
    organizations_db_table = session.query(Organizations).all()
    organizations_list_of_dicts = []
    for each_record in organizations_db_table:
        organizations_list_of_dicts.append(
            {'id': str(each_record.id),
             'role': each_record.role,
             'status': each_record.status,
             'okopf': each_record.okopf,
             'full_name': each_record.full_name,
             'short_name': each_record.short_name,
             'firm_name': each_record.firm_name,
             'inn': each_record.inn,
             'ogrn': each_record.ogrn,
             'kpp': each_record.kpp,
             'address': each_record.address,
             'phone': each_record.phone,
             'email': each_record.email,
             'registered_at': each_record.registered_at,
             'blocked_at': each_record.blocked_at,
             'created_at': each_record.created_at,
             'updated_at': each_record.updated_at,
             }
        )
    if len(organizations_list_of_dicts) > 0:
        return organizations_list_of_dicts
    else:
        return False
