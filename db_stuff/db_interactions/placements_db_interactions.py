from db_stuff.sqlalchmy_interactions import establish_postgresql_connection
from db_stuff.models.db_models import Placements


def delete_placements_record(_uuid: str):
    """Удаление размещения в бд у конкретного медиаплана"""
    session = establish_postgresql_connection()
    session.query(Placements).filter_by(mplan_id=_uuid).delete()
    session.commit()
    session.close()