import allure
import pytest

from admin_office.components.pages.products.products_page import AdminOfficeProductsPage
from admin_office.constants import LIMIT_OF_ROWS_ON_ONE_PAGE_IN_PRODUCTS
from admin_office.api_interactions.products.products_api_interactions import get_count_of_products
from admin_office.tests.api.dictionaries.products.data_make_for_products import make_data_all_product_fields
from db_stuff.db_interactions.products_db_interactions import get_product_id_by_naming
from admin_office.api_interactions.products.products_api_interactions import delete_product_by_id
from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira

data_product = make_data_all_product_fields()


@pytest.fixture()
def clean_up_products_data(
    authorization_in_admin_office_with_token,
):
    """ Удаляет данные после выполнения всех тестов """
    token = authorization_in_admin_office_with_token
    created_product_id = get_product_id_by_naming(data_product['naming'])
    if created_product_id:
        delete_product_by_id(created_product_id, token)


@pytest.mark.usefixtures('authorization_in_admin_office_with_token')
class TestProducts:
    @staticmethod
    @pytest.mark.smoke
    @allure.title('Справочник Продукты')
    @allure.story(jira.JIRA_LINK + 'MDP-1696')
    @allure.testcase(case.ALLURE_LINK + '225254')
    def test_view_products(
            admin_base_url: str,
            admin_products_page: AdminOfficeProductsPage,
            authorization_in_admin_office_with_token: str,
    ):
        """Справочник Продукты"""
        token = authorization_in_admin_office_with_token
        admin_products_page.go_to_products()
        count_all_rows = len(get_count_of_products(token))
        admin_products_page.products.check_quantity_products(count_all_rows)
        admin_products_page.products.check_transition_to_next_page(
            count_all_rows
        )
        count_rows_in_second_page = (
            count_all_rows
            if count_all_rows <= LIMIT_OF_ROWS_ON_ONE_PAGE_IN_PRODUCTS
            else count_all_rows - LIMIT_OF_ROWS_ON_ONE_PAGE_IN_PRODUCTS
        )
        admin_products_page.products.check_quantity_products(
            count_rows_in_second_page
        )
        admin_products_page.visit(admin_base_url + "/dictionaries/products")

    @staticmethod
    @pytest.mark.smoke
    @allure.title('Создание записи в справочнике Продукт')
    @allure.story(jira.JIRA_LINK + 'MDP-760')
    @allure.testcase(case.ALLURE_LINK + '131193')
    def test_create_product(
            admin_products_page: AdminOfficeProductsPage,
            authorization_in_admin_office_with_token: str,
    ):
        """Создание записи в справочнике Продукт"""
        admin_products_page.products.open_the_product_creation_form()
        admin_products_page.product_card.fill_all_fields(**data_product)
        admin_products_page.product_card.save_product()
        admin_products_page.products.check_new_product(data_product)

    @staticmethod
    @pytest.mark.smoke
    @allure.title("Редактирование через карточку продукта")
    @allure.story(jira.JIRA_LINK + 'MDP-1166')
    @allure.testcase(case.ALLURE_LINK + '131297')
    def test_edit_product(
            admin_base_url: str,
            admin_products_page: AdminOfficeProductsPage,
            authorization_in_admin_office_with_token: str,
    ):
        created_product_id = get_product_id_by_naming(data_product['naming'])
        admin_products_page.products.page.get_by_role('row', name=created_product_id).get_by_role(
            'link').click()
        admin_products_page.product_card.fill_product_name_field(data_product['name'] + 'ed1')
        data_product["name"] = data_product["name"] + "ed1"
        admin_products_page.product_card.save_product()
        admin_products_page.products.page.reload(wait_until='load')
        admin_products_page.products.check_new_product(data_product)

    @staticmethod
    @pytest.mark.smoke
    @allure.title("Редактирование через контекстное меню записи в справочнике 'Продукты'")
    @allure.story(jira.JIRA_LINK + 'MDP-1166')
    @allure.testcase(case.ALLURE_LINK + '131297')
    def test_edit_product_context_menu(
            admin_base_url: str,
            admin_products_page: AdminOfficeProductsPage,
            authorization_in_admin_office_with_token: str,
    ):
        token = authorization_in_admin_office_with_token
        created_product_id = get_product_id_by_naming(data_product['naming'])
        admin_products_page.products.page.get_by_role('row', name=created_product_id).get_by_role(
            'button').click()
        admin_products_page.products.page.get_by_role("button", name="Редактировать").click()
        admin_products_page.product_card.fill_product_name_field(data_product['name'] + 'ed2')
        data_product["name"] = data_product["name"] + "ed2"
        admin_products_page.product_card.save_product()
        admin_products_page.products.page.reload(wait_until='load')
        admin_products_page.products.check_new_product(data_product)

    @staticmethod
    @pytest.mark.smoke
    @allure.title("Удаление записи в справочнике 'Продукты' через карточку продукта")
    @allure.story(jira.JIRA_LINK + 'MDP-1166')
    @allure.testcase(case.ALLURE_LINK + '131296')
    def test_delete_product(
            admin_base_url: str,
            admin_products_page: AdminOfficeProductsPage,
    ):
        created_product_id = get_product_id_by_naming(data_product['naming'])
        admin_products_page.products.page.get_by_role('row', name=created_product_id).get_by_role(
            'link').click()
        admin_products_page.product_card.click_delete_button_product_card()
        admin_products_page.page.get_by_test_id("dialog_confirm").click()
        assert get_product_id_by_naming(data_product["naming"]) is False, "Запись не удалена"

    @staticmethod
    @pytest.mark.smoke
    @allure.title("Удаление через контекстное меню записи в справочнике 'Продукты'")
    @allure.story(jira.JIRA_LINK + 'MDP-1166')
    @allure.testcase(case.ALLURE_LINK + '131296')
    def test_delete_product_context_menu(
            admin_base_url: str,
            admin_products_page: AdminOfficeProductsPage,
            clean_up_products_data,
    ):
        admin_products_page.products.open_the_product_creation_form()
        admin_products_page.product_card.fill_all_fields(**data_product)
        admin_products_page.product_card.save_product()
        admin_products_page.products.check_new_product(data_product)
        created_product_id = get_product_id_by_naming(data_product['naming'])
        admin_products_page.products.page.get_by_role('row', name=created_product_id).get_by_role(
            'button').click()
        admin_products_page.products.page.get_by_role("button", name="Удалить").click()
        admin_products_page.page.get_by_test_id("dialog_confirm").click()
        assert get_product_id_by_naming(data_product["naming"]) is False, "Запись не удалена"
