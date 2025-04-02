import re
import uuid

from sqlalchemy import insert

from db_stuff.sqlalchmy_interactions import establish_postgresql_connection_for_reporting_db, \
    establish_postgresql_connection
from db_stuff.models.db_reporting_models import ConversionPtrs
from db_stuff.models.db_models import MplanConversions


def insert_external_parent_id_in_conversion_ptrs() -> str:
    session = establish_postgresql_connection_for_reporting_db()
    id = '13540021'
    external_id = uuid.uuid4()
    name = 'YANDEX_METRIC_IN_POST_CLICK_DONT_DELETE'
    source_type = 'POSTCLICK'
    source_code = 'YM'
    is_valid = True
    external_parent_id = '219235111'

    session.scalars(
        insert(ConversionPtrs)
        .values(
            [
                {
                    'id': id,
                    'external_id': external_id,
                    'name': name,
                    'source_type': source_type,
                    'source_code': source_code,
                    "is_valid": is_valid,
                    "external_parent_id": external_parent_id,
                },
            ]
        )
        .returning(ConversionPtrs)
    )


def get_metric(metric_name: str) -> str:
    session = establish_postgresql_connection()
    name = session.query(MplanConversions).filter(MplanConversions.name == metric_name).first()
    """
    Ниже регулярка очищающая строку от спец симолов
        :return возвращается uuid в чистом виде - 345345f3-3534-5fff44-345f35-45f43
    """
    pattern = "[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"
    string = re.findall(pattern, str(name))
    replacements = [('(UUID(', ''), ('))', ''), ('[]', '')]
    for char, replacement in replacements:
        if char in string:
            string = string.replace(char, replacement)
        braces = {'[', ']'}
        s = ''.join(ch for ch in string if ch not in braces)
    return s
