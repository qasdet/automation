import allure
import pytest

from admin_office.components.pages.brands.brands_page import (
    AdminOfficeBrandsPage,
)
from admin_office.constants import LIMIT_OF_ROWS_ON_ONE_PAGE_IN_BRANDS
from admin_office.api_interactions.brands.brands_api_interactions import (
    delete_brand_by_id,
    get_count_of_brands,
)
from admin_office.tests.api.dictionaries.brands.data_make_for_brands import (
    make_data_all_brand_fields,
)
from db_stuff.db_interactions.brands_db_interactions import get_brand_by_naming
from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira


@pytest.fixture()
def life_cycle_of_the_brand_with_all_field(
    authorization_in_admin_office_with_token,
):
    data_brand = make_data_all_brand_fields()
    yield data_brand
    token = authorization_in_admin_office_with_token
    brand = get_brand_by_naming(data_brand['naming'])
    if brand:
        delete_brand_by_id(brand.id, token)


@pytest.mark.usefixtures('authorization_in_admin_office_with_token')
class TestsBrands:
    @staticmethod
    @pytest.mark.smoke
    @allure.title('Справочник Бренды')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story(jira.JIRA_LINK + 'MDP-759')
    @allure.testcase(case.ALLURE_LINK + '175387')
    def test_view_brands(
        admin_base_url: str,
        admin_brands_page: AdminOfficeBrandsPage,
        authorization_in_admin_office_with_token: str,
    ):
        """Справочник Бренды"""
        token = authorization_in_admin_office_with_token
        admin_brands_page.go_to_brands()
        count_all_rows = get_count_of_brands(token)
        admin_brands_page.brands.check_quantity_brands(count_all_rows)
        admin_brands_page.brands.check_transition_to_next_page(count_all_rows)
        count_rows_in_second_page = (
            count_all_rows
            if count_all_rows <= LIMIT_OF_ROWS_ON_ONE_PAGE_IN_BRANDS
            else count_all_rows - LIMIT_OF_ROWS_ON_ONE_PAGE_IN_BRANDS
        )
        admin_brands_page.brands.check_quantity_brands(
            count_rows_in_second_page
        )
        admin_brands_page.visit(admin_base_url + "/dictionaries/brands")

    @pytest.mark.smoke
    @allure.title('Создание записи в справочнике Бренды')
    @allure.story(jira.JIRA_LINK + 'MDP-759')
    @allure.testcase(case.ALLURE_LINK + '159670')
    def test_create_brand(
        self,
        admin_brands_page: AdminOfficeBrandsPage,
        life_cycle_of_the_brand_with_all_field,
    ):
        """Создание записи в справочнике Бренды"""
        data_brand = life_cycle_of_the_brand_with_all_field
        admin_brands_page.go_to_brands()
        admin_brands_page.brands.open_the_brand_creation_form()
        admin_brands_page.card_brand.fill_all_fields(**data_brand)
        admin_brands_page.card_brand.save_brand()
        admin_brands_page.brands.check_new_brand(data_brand)
