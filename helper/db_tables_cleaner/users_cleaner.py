from db_stuff.db_interactions.persons_db_interactions import get_persons_by_organization_id
from db_stuff.db_interactions.users_db_interactions import get_user_by_person_id
from db_stuff.db_interactions.persons_db_interactions import delete_person_by_id
from db_stuff.db_interactions.users_db_interactions import delete_user_by_id


def clean_records(organization_id_value: str) -> None:
    """
    Собирает записи, которые принадлежат конкретной организации в таблицах persons и users,
    затем удаляет их.
    Args
        organization_id_value: уникальный номер организации
    """
    records_from_persons_table = get_persons_by_organization_id(organization_id_value)
    persons_records_ids_only = []
    users_records_ids_only = []
    for each_record in records_from_persons_table:
        persons_records_ids_only.append(each_record['id'])
        getting_dict_from_users_table_record = get_user_by_person_id(each_record['id'])
        users_records_ids_only.append(getting_dict_from_users_table_record[0]['id'])
    if persons_records_ids_only == users_records_ids_only:
        for each_record in persons_records_ids_only:
            delete_person_by_id(each_record)
        for each_record in users_records_ids_only:
            delete_user_by_id(each_record)
    else:
        print("These lists are not equal!")
