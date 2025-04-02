import allure
import pytest

from admin_office.api_interactions.product_price_categories.product_price_categories_api_interactions import (
    get_list_of_product_price_categories,
)
from db_stuff.db_interactions.product_price_categories_db_interactions import (
    get_list_of_the_product_price_categories_from_db,
)
from helper.linkshort import JiraLink as jira


@pytest.mark.usefixtures('authorization_in_admin_office_with_token')
class TestsProductPriceCategoriesAPI:
    @staticmethod
    @pytest.mark.regress()
    @allure.title('Получение всех записей через API')
    @allure.story(jira.JIRA_LINK + 'MDP-770')
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_all_records(authorization_in_admin_office_with_token) -> None:
        """Получение всех записей"""
        token = authorization_in_admin_office_with_token
        product_price_categories_service = get_list_of_product_price_categories(token)
        product_price_categories_service.sort(
            key=lambda dictionary: dictionary['code']
        )
        product_price_categories_db = (
            get_list_of_the_product_price_categories_from_db()
        )
        product_price_categories_db.sort(
            key=lambda dictionary: dictionary['code']
        )
        assert (
            product_price_categories_service == product_price_categories_db
        ), 'Данные с сервиса не совпадают с данными из БД'
