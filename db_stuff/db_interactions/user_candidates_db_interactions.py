from db_stuff.sqlalchmy_interactions import establish_postgresql_connection_for_user_cand_db
from db_stuff.models.db_candidate_models import UserCandidates


def get_list_of_the_user_candidates_from_db() -> list:
    """Получение всех записей из БД

    Returns:
        список записей
    """
    session = establish_postgresql_connection_for_user_cand_db()
    rows = (
        session.query(UserCandidates)
        .filter(UserCandidates.deleted_at == None)
        .order_by(UserCandidates.created_at.desc())
        .all()
    )
    session.close()
    resulted_list = []
    for each_record in rows:
        resulted_list.append(
            {
                'id': str(each_record.id),
                'name': each_record.name,
                'surname': each_record.surname,
                'email': each_record.email,
                'phone': each_record.phone,
                'firmName': each_record.firm_name,
                'role': each_record.role,
                "isPerformed": each_record.is_performed,
                'created_at': each_record.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            }
        )
    return resulted_list


def get_specific_user_candidate_id(surname_value: str) -> list:
    """Получение уникального номера созданной заявки по фамилии пользователя
    Arguments:
        surname_value: фамилия в созданной заявке. Она содержит небольшой хэш, что делает каждую запись уникальной
    Returns:
        Уникальный номер созданной заявки
    """

    session = establish_postgresql_connection_for_user_cand_db()
    row = (
        session.query(UserCandidates)
        .filter(UserCandidates.deleted_at == None, UserCandidates.surname == surname_value)
        .all()
    )
    session.close()
    return row[0].id


def get_date_if_record_was_deleted(surname_value: str) -> bool:
    """Проверка даты удаления записи, что она там появляется после удаления записи через АПИ
    Arguments:
        surname_value: фамилия в созданной заявке. Она содержит небольшой хэш, что делает каждую запись уникальной
    Returns:
        True or False
    """
    session = establish_postgresql_connection_for_user_cand_db()
    row = session.query(UserCandidates.deleted_at).filter(UserCandidates.surname == surname_value).all()
    session.close()
    result = row[0].deleted_at
    if result:
        return True
    else:
        return False


def get_data_of_the_user_candidates_by_id_from_db(
        user_candidates_id: int,
) -> dict:
    """Получение записи из БД по id
    Args:
        user_candidates_id: id записи
    Returns:
        Словарь данных записи
    """
    session = establish_postgresql_connection_for_user_cand_db()
    row = (
        session.query(UserCandidates)
        .filter(UserCandidates.id == user_candidates_id)
        .one()
    )
    session.close()
    return {
        'id': row.id,
        'name': row.name,
        'surname': row.surname,
        'email': row.email,
        'phone': row.phone,
        'firm_name': row.firm_name,
        'role': row.role,
        'comments': row.comments,
        "isPerformed": row.isPerformed,
        'created_at': row.created_at.strftime('%Y-%m-%dT%H:%M'),
        'deleted_at': row.deleted_at.strftime('%Y-%m-%dT%H:%M')
        if row.deleted_at is not None
        else None,
    }
