import math

from db_stuff.sqlalchmy_interactions import establish_postgresql_connection
from db_stuff.models.db_models import Users, Persons


def delete_user_by_id(user_id_value: str) -> None:
    """Удалить запись из таблицы users по уникальному номеру
    Args:
        user_id_value: уникальный номер записи в таблице записи в таблице
    """
    session = establish_postgresql_connection()
    session.query(Users).filter(Users.id == user_id_value).delete()
    session.commit()
    session.close()


def get_user_by_login_and_phone_and_email(
        login: str, phone: str, email: str
) -> Users:
    """Получить пользователя из БД по логину, телефону и email
    Args:
        login Логин
        phone Пароль
        email Почтовый ящик
    Returns:
        Пользователь
    """
    session = establish_postgresql_connection()
    row = (
        session.query(Users)
        .filter(
            Users.login == login
            and Users.phone == phone
            and Users.email == email
        )
        .first()
    )
    session.close()
    return row


def get_the_number_of_pages_in_the_user_directory(amount: int = 10) -> int:
    """Вычисляет количество страниц в Пользователях
    Args:
        amount количество записей на одной странице (по умолчанию 10)
    """
    session = establish_postgresql_connection()
    count = session.query(Users).count()
    session.close()
    return math.ceil(count / amount)


def get_users_list_db() -> list | bool:
    """Получить список пользователей из таблицы users
    Returns:
        Список пользователей из таблицы users
    """
    session = establish_postgresql_connection()
    users_list = session.query(Users).all()
    users_list_of_dicts = []
    if len(users_list) > 0:
        for each_record in users_list:
            users_list_of_dicts.append(
                {'id': str(each_record.id),
                 'status': each_record.status,
                 'login': each_record.login,
                 'email': each_record.email,
                 'phone': each_record.phone,
                 'registered_at': each_record.registered_at.strftime('%Y-%m-%dT%H:%M:%S'),
                 'blocked_at': each_record.blocked_at if
                 each_record.blocked_at is None
                 else each_record.blocked_at.strftime('%Y-%m-%dT%H:%M:%S'),
                 }
            )
        return users_list_of_dicts
    else:
        return False


def get_user_by_person_id(person_id_value: str) -> list | bool:
    """Получить запись из таблицы users, которая найдена по идентификатору из таблицы persons
    Args:
        person_id_value: уникальный номер пользователя
    Returns:
        Список пользователей из таблицы users, у которых есть соответствия в таблице persons.
    """
    session = establish_postgresql_connection()
    users_db_table = session.query(Users).filter(Users.id == person_id_value).all()
    users_list_of_dicts = []
    for each_record in users_db_table:
        users_list_of_dicts.append(
            {'id': str(each_record.id),
             'status': each_record.status,
             'login': each_record.login,
             'email': each_record.email,
             'phone': each_record.phone,
             'registered_at': each_record.registered_at,
             'created_at': each_record.created_at,
             'blocked_at': each_record.blocked_at,
             'order_no': each_record.order_no,
             'updated_at': each_record.updated_at,
             }
        )
    if len(users_list_of_dicts) > 0:
        return users_list_of_dicts
    else:
        return False


def united_list_users_and_persons_by_organization_id(organization_id_value: str) -> list:
    """Получить составной список пользователей из таблиц users и persons по уникальному номеру организации
    Args:
        organization_id_value: уникальный номер организации
    Returns:
        Пользователь
    """
    session = establish_postgresql_connection()
    persons = (
        session.query(Persons)
        .filter(Persons.organization_id == organization_id_value)
        .all()
    )
    users = []
    for person in persons:
        user = session.query(Users).filter(Users.id == person.id).first()
        users.append(
            {
                'id': str(user.id),
                'login': user.login,
                'email': user.email,
                'phone': user.phone,
                'status': user.status,
                'name': person.name,
                'surname': person.surname,
                'middleName': person.middle_name,
            }
        )
    session.close()
    return users
