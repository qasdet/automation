from sqlalchemy import select
from db_stuff.models.db_models import Mplans
from db_stuff.sqlalchmy_interactions import establish_postgresql_connection


def widget_in_mplan_unique_number(*order_number) -> str:
    session = establish_postgresql_connection()
    stmt = (select(
        Mplans.order_no).where(Mplans.id == order_number)
            )
    r = session.execute(stmt)
    return str(*r.first())