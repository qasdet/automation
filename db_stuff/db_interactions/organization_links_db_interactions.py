from db_stuff.sqlalchmy_interactions import establish_postgresql_connection
from db_stuff.models.db_models import OrganizationLinks, Brands, Clients, Products


def get_organization_links_data_by_organization_id(organization_id_value: str) -> list:
    """Получить данные связей брендов, клиентов, продуктов для справочников из таблицы organization_links
     по уникальному номеру организации
        Args:
            organization_id_value: уникальный номер организации
        Returns:
            Данные связей для справочников(списки из списков внутри списка)
    """
    session = establish_postgresql_connection()
    organization_links_dict_data = (
        session.query(Clients.name + ' ' + Clients.naming, Brands.name + ' ' + Brands.naming,
                      Products.name + ' ' + Products.naming)
        .select_from(OrganizationLinks)
        .outerjoin(Clients, Clients.id == OrganizationLinks.client_id)
        .outerjoin(Brands, Brands.id == OrganizationLinks.brand_id)
        .outerjoin(Products, Products.id == OrganizationLinks.product_id)
        .filter(OrganizationLinks.organization_id == organization_id_value)
        .order_by(OrganizationLinks.created_at, Brands.naming, Products.naming)
        .all()
    )
    # заменяем None на ""
    formatted_organization_links_dict_data = [
        list("" if x is None else x for x in row)
        for row in organization_links_dict_data
    ]
    # делим выборку на списки с маскимальной вместительностью 10 шт, как на странице справочника
    result = [formatted_organization_links_dict_data[i:i + 10] for i in range(
        0, len(formatted_organization_links_dict_data), 10
    )]
    return result
