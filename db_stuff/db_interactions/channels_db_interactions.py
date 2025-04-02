from db_stuff.sqlalchmy_interactions import establish_postgresql_connection
from db_stuff.models.db_models import Channels


def get_list_of_channels_from_db():
    """Получение всех записей из БД

    Returns:
        список записей
    """
    session = establish_postgresql_connection()
    list_channel = session.query(Channels).all()
    result = [
        {
            'name': row.name,
            'code': row.code,
            'media_type': row.media_type,
            'is_used_by_splan': row.is_used_by_splan,
            'naming': row.naming,
        }
        for row in list_channel
    ]
    return sorted(result, key=lambda x: x['code'])


def get_channel_by_naming(naming_value: str) -> Channels:
    """Получить канал из БД по неймингу
    Args:
        naming_value: нейминг
    Returns:
        Канал
    """
    session = establish_postgresql_connection()
    row = session.query(Channels).filter(Channels.naming == naming_value).first()
    session.close()
    return row


def get_channel_name_by_naming(naming_value: str) -> str | bool:
    """Получить название канала из БД по неймингу
    Args:
        naming_value: нейминг
    Returns:
        Название канала
    """
    session = establish_postgresql_connection()
    row = session.query(Channels.name).filter(Channels.naming == naming_value).first()
    session.close()
    return row[0]


def get_channel_by_code(code_value: str) -> Channels:
    """Получить канал из БД по неймингу
    Args:
        code_value: нейминг
    Returns:
        Канал
    """
    session = establish_postgresql_connection()
    row = session.query(Channels).filter(Channels.code == code_value).first()
    session.close()
    return row


def delete_channel_by_naming(channel_naming_value: str) -> None:
    """Удалить канал по неймингу
    Args:
        channel_naming_value: нейминг канала
    """
    session = establish_postgresql_connection()
    session.query(Channels).filter(Channels.naming == channel_naming_value).delete()
    session.commit()
    session.close()


def delete_channel_by_code(channel_code_value: str) -> None:
    """Удалить канал по неймингу
    Args:
        channel_code_value: код канала
    """
    session = establish_postgresql_connection()
    session.query(Channels).filter(Channels.code == channel_code_value).delete()
    session.commit()
    session.close()
