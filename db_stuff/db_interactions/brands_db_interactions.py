from db_stuff.sqlalchmy_interactions import establish_postgresql_connection
from db_stuff.models.db_models import Brands, BrandAwarenesses


def get_brand_by_naming(naming: str) -> Brands:
    """Получить бренд из БД по коду. Применимо и для ко-брендов
    Args:
        naming: нейминг
    Returns:
        Бренд
    """
    session = establish_postgresql_connection()
    row = session.query(Brands).filter(Brands.naming == naming).first()
    session.close()
    return row


def get_brand_id_by_naming(naming: str) -> str:
    """Получить id бренда из БД по неймингу. Применимо и для ко-брендов
    Args:
        naming: нейминг
    Returns:
        id бренда
    """
    session = establish_postgresql_connection()
    row = session.query(Brands.id).filter(Brands.naming == naming).first()
    session.close()
    if row[0] != '':
        return row[0]
    else:
        return ''


def get_brand_name_by_id(brand_id: str) -> Brands:
    """Получить наименование бренда из БД по id. Применимо и для ко-брендов
    Args:
        brand_id: id бренда
    Returns:
        наименование бренда
    """
    session = establish_postgresql_connection()
    row = session.query(Brands.name).filter(Brands.id == brand_id).first()
    session.close()
    return row[0]


def get_brands_data_by_organization_id(organization_id_value: str) -> list:
    """Получить данные брендов для справочников из таблицы brands по уникальному номеру организации
        Применимо и для ко-брендов
        Args:
            organization_id_value: уникальный номер организации
        Returns:
            Данные брендов для справочников(списки из списков внутри списка)
    """
    session = establish_postgresql_connection()
    brands_dict_data = (
        session.query(Brands.name, Brands.naming, BrandAwarenesses.name)
        .outerjoin(BrandAwarenesses, Brands.awareness_id == BrandAwarenesses.id)
        .filter(
            (Brands.acl_organization_id == organization_id_value) and
            ((BrandAwarenesses.id == Brands.awareness_id) | (BrandAwarenesses.id.is_(None)))
        )
        .order_by(Brands.name)
        .all()
    )
    # заменяем None на ""
    formatted_brands_dict_data = [
        list("" if x is None else x for x in row)
        for row in brands_dict_data
    ]
    # делим выборку на списки с маскимальной вместительностью 10 шт, как на странице справочника
    result = [formatted_brands_dict_data[i:i + 10] for i in range(0, len(formatted_brands_dict_data), 10)]
    return result
