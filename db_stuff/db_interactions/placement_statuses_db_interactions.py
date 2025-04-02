from db_stuff.sqlalchmy_interactions import establish_postgresql_connection
from db_stuff.models.db_models import Placements, PlacementStatuses

from sqlalchemy import select, and_

def get_list_of_the_placement_statuses_from_db(
        without_id: bool = False,
) -> list:
    """Получение всех записей из БД

    Args:
        without_id: возвращать список без id

    Returns:
        список записей
    """
    session = establish_postgresql_connection()
    rows = (
        session.query(PlacementStatuses).order_by(PlacementStatuses.id).all()
    )
    session.close()
    if without_id:
        return [{'name': row.name, 'code': row.code} for row in rows]
    else:
        return [
            {
                'id': str(row.id),
                'name': row.name,
                'code': row.code,
            }
            for row in rows
        ]


def get_name_status_by_id_of_placements_status_id_in_the_placement(placement_id):
    """Получение текстового представления статус размещения

        Args:
            placement_id: uuid размещения

        Returns:
            текстовое представление статус размещения: UUID размещения и статус Уточнение настроек
        """
    with establish_postgresql_connection() as session:
        r = session.query(Placements.placement_status_id, PlacementStatuses.name).select_from(
            Placements, PlacementStatuses).filter(Placements.placement_status_id ==
                                                  PlacementStatuses.id).filter(and_(Placements.id == placement_id))
        return str(r.first())

