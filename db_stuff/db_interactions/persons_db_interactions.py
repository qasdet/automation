from db_stuff.sqlalchmy_interactions import establish_postgresql_connection
from db_stuff.models.db_models import Persons


def delete_person_by_id(person_id_value: str) -> None:
    """Удалить запись из таблицы persons по уникальному номеру
    Args:
        person_id_value: уникальный номер записи в таблице записи в таблице
    """
    session = establish_postgresql_connection()
    session.query(Persons).filter(Persons.id == person_id_value).delete()
    session.commit()
    session.close()


def get_person_by_name(person_name_value: str) -> dict | bool:
    """Получить уникальный номер пользователя из таблицы persons по имени пользователя
    Args:
        person_name_value: уникальный номер пользователя
    Returns:
        Данные одного пользователя, полученные по его имени
    """
    session = establish_postgresql_connection()
    row = session.query(Persons).filter(Persons.name == person_name_value).first()
    if row:
        return dict(id=str(row.id),
                    organization_id=str(row.organization_id),
                    name=row.name,
                    surname=row.surname,
                    middle_name=row.middle_name)
    else:
        return False


def get_persons_list_db() -> list | bool:
    """Получить список пользователей из таблицы persons
    Returns:
        Список пользователей из таблицы users
    """
    session = establish_postgresql_connection()
    persons_list = session.query(Persons).all()
    persons_list_of_dicts = []
    if len(persons_list) > 0:
        for each_record in persons_list:
            persons_list_of_dicts.append(
                {'id': str(each_record.id),
                 'surname': each_record.surname,
                 'name': each_record.name,
                 'organization_id': str(each_record.organization_id),
                 'middle_name': each_record.middle_name,
                 'contact_phone': each_record.contact_phone,
                 'created_at': each_record.created_at.strftime('%Y-%m-%dT%H:%M:%S'),
                 'updated_at': each_record.updated_at.strftime('%Y-%m-%dT%H:%M:%S'),
                 }
            )
        return persons_list_of_dicts
    else:
        return False


def get_persons_by_organization_id(organization_id_value: str) -> list | bool:
    """Получить список пользователей из таблицы persons по уникальному номеру организации
    Args:
        organization_id_value: уникальный номер организации
    Returns:
        Cписок пользователей, соответствующей конкретной организации
    """
    session = establish_postgresql_connection()
    persons_db_table = session.query(Persons).filter(Persons.organization_id == organization_id_value).all()
    persons_list_of_dicts = []
    for each_record in persons_db_table:
        persons_list_of_dicts.append(
            {'id': str(each_record.id),
             'organization_id': str(each_record.organization_id),
             'name': each_record.name,
             'middle_name': each_record.middle_name,
             'surname': each_record.surname,
             'created_at': each_record.created_at,
             'updated_at': each_record.updated_at,
             'contact_phone': each_record.contact_phone}
        )
    if len(persons_list_of_dicts) > 0:
        return persons_list_of_dicts
    else:
        return False
