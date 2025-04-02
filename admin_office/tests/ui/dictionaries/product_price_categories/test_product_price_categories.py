import allure
import pytest

from admin_office.components.pages.product_price_categories.product_price_categories_page import (
    AdminOfficeProductPriceCategoriesPage,
)
from db_stuff.db_interactions.product_price_categories_db_interactions import (
    get_list_of_the_product_price_categories_from_db,
)
from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira


# TODO Переписать согласно новой концепции
@pytest.mark.usefixtures('authorization_in_admin_office')
class TestsProductPriceCategoriesUI:
    @staticmethod
    @pytest.mark.regress()
    @allure.title('Справочник Статусы размещений')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story(jira.JIRA_LINK + 'MDP-770')
    @allure.testcase(case.ALLURE_LINK + '149516')
    def test_view_product_price_categories(
        admin_product_price_categories_page: AdminOfficeProductPriceCategoriesPage,
    ) -> None:
        """Справочник Ценовые категории продукта"""
        admin_product_price_categories_page.go_to_product_price_categories()
        product_price_categories_db = (
            get_list_of_the_product_price_categories_from_db()
        )
        table = (
            admin_product_price_categories_page.product_price_categories.table
        )
        for index, row_db in enumerate(product_price_categories_db):
            table.should_have_text_cell_in_row_by_contains_text(
                text_row=str(row_db['id']),
                number_cell=0,
                check_text=str(row_db['id']),
            )
            table.should_have_text_cell_in_row_by_contains_text(
                text_row=str(row_db['id']),
                number_cell=1,
                check_text=str(row_db['name']),
            )
            table.should_have_text_cell_in_row_by_contains_text(
                text_row=str(row_db['id']),
                number_cell=2,
                check_text=str(row_db['code']),
            )
