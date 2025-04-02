from typing import TypeVar
from db_stuff.sqlalchmy_interactions import establish_postgresql_connection
from db_stuff.models.db_models import Products

_T = TypeVar(str)


def check_product_record(name_p: _T):
    """Запрос на проверку наличия бренда в бд"""
    session = establish_postgresql_connection()
    q = session.query(Products).filter_by(name=name_p)
    return q.first()


def create_product_record(name_p: _T, naming_p: _T, code_p: _T, seasonality_p_id: _T, prf_id: _T, type_p_id: _T,
                          prc_p_id: _T, cat_p_id: _T, geo_p_id: _T, acl_org_id: _T):
    """
    Если бренда нет, то бренда создается
    На вход принимаются следующие параметры:
        :name='Autotest Product', имя продукта
        :naming='AUTOTESTP',
        :code='AUTOTESTP',
        :seasonality_id='33c9441f-a4a0-457a-8aa9-09ca4127781f',
        :purchase_frequency_id='dd0d636b-0bec-434b-b6fe-676328281978',
        :type_id="fde0c23a-5471-46ee-bb18-1a6f39c65eaf",
        :price_category_id="f703635a-1317-47a5-a40e-99f8c4951005",
        :category_id="6fdef78e-75e6-4d45-a078-5c86b3f026bd",
        :geography_id="c358ce52-3ed2-4c2f-81d9-f26a0aa8f138",
        :acl_organization_id="5b872b04-9bf9-4665-8a6c-9e137fd67066",
    """

    session = establish_postgresql_connection()
    validation_brands = Products(
        name=name_p,
        naming=naming_p,
        code=code_p,
        seasonality_id=seasonality_p_id,
        purchase_frequency_id=prf_id,
        type_id=type_p_id,
        price_category_id=prc_p_id,
        category_id=cat_p_id,
        geography_id=geo_p_id,
        acl_organization_id=acl_org_id
    )
    session.add(validation_brands)
    session.commit()
    session.rollback()
    session.close()


def delete_product_record(naming_p: _T):
    """Удаление записи бренда из бд"""
    session = establish_postgresql_connection()
    session.query(Products).filter_by(name=naming_p).delete()
    session.commit()
    session.close()
