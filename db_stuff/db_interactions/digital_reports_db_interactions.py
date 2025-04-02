from db_stuff.sqlalchmy_interactions import establish_postgresql_connection_for_reporting_db
from db_stuff.models.db_reporting_models import DigitalReports


def get_digital_report_by_campaign_id(campaign_id: str) -> DigitalReports:
    """Получить данные отчета план-факт
    Args:
        campaign_id: id кампании
    Returns:
        Данные отчета план-факт
    """
    session = establish_postgresql_connection_for_reporting_db()
    row = session.query(DigitalReports.data).filter(DigitalReports.campaign_id == campaign_id).first()
    session.close()
    return row[0]
