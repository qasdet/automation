import allure
import pytest
import humps

from admin_office.components.pages.clients.clients_page import (
    AdminOfficeClientsPage,
)
from admin_office.constants import LIMIT_OF_ROWS_ON_ONE_PAGE_IN_CLIENTS
from admin_office.api_interactions.clients.clients_api_interactions import (
    get_clients_api,
    get_client_info,
)
from admin_office.tests.api.dictionaries.clients.data_make_for_client import (
    make_data_all_client_fields,
)
from db_stuff.db_interactions.clients_db_interactions import get_client_by_naming
from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira

data_client = humps.decamelize(make_data_all_client_fields())
edit_sign = '_ED'


@pytest.mark.usefixtures('authorization_in_admin_office_with_token')
class TestClientsUI:
    @staticmethod
    @pytest.mark.smoke
    # @pytest.mark.order(1)
    @allure.title('Справочник Клиенты')
    @allure.story(jira.JIRA_LINK + 'MDP-1168')
    @allure.testcase(case.ALLURE_LINK + '195066')
    def test_view_clients(
            admin_base_url: str,
            admin_clients_page: AdminOfficeClientsPage,
            authorization_in_admin_office_with_token: str,
    ):
        """Справочник Клиенты"""
        token = authorization_in_admin_office_with_token
        admin_clients_page.go_to_clients()
        count_all_rows = len(get_clients_api(token))
        admin_clients_page.clients.check_quantity_clients(count_all_rows)
        admin_clients_page.clients.check_transition_to_next_page(
            count_all_rows
        )
        count_rows_in_second_page = (
            count_all_rows
            if count_all_rows <= LIMIT_OF_ROWS_ON_ONE_PAGE_IN_CLIENTS
            else count_all_rows - LIMIT_OF_ROWS_ON_ONE_PAGE_IN_CLIENTS
        )
        admin_clients_page.clients.check_quantity_clients(
            count_rows_in_second_page
        )
        admin_clients_page.visit(admin_base_url)

    @staticmethod
    @pytest.mark.smoke
    # @pytest.mark.order(2)
    @allure.title('Создание записи в справочнике Клиенты')
    @allure.story(jira.JIRA_LINK + 'MDP-1168')
    @allure.testcase(case.ALLURE_LINK + '195067')
    def test_create_client(
            admin_base_url: str,
            admin_clients_page: AdminOfficeClientsPage,
            authorization_in_admin_office_with_token,
    ):
        """Создание записи в справочнике Клиенты"""
        admin_clients_page.go_to_clients()
        admin_clients_page.clients.open_the_client_creation_form()
        admin_clients_page.client_card.fill_all_fields(**data_client)
        admin_clients_page.client_card.save_client()
        admin_clients_page.clients.check_new_client(data_client)
        admin_clients_page.page.goto(admin_base_url + "/dictionaries/clients")

    @staticmethod
    @pytest.mark.smoke
    # @pytest.mark.order(3)
    @allure.title('Редактирование записи в справочнике Клиенты')
    @allure.story(jira.JIRA_LINK + 'MDP-1168')
    @allure.testcase(case.ALLURE_LINK + '195067')
    def test_edit_client(
            admin_clients_page: AdminOfficeClientsPage,
    ):
        created_client_id = str(get_client_by_naming(data_client['naming']).id)
        admin_clients_page.page.get_by_role('row', name=created_client_id).get_by_role(
            'button').click()
        admin_clients_page.page.get_by_role("button", name="Редактировать").click()
        admin_clients_page.page.get_by_test_id("client_card_name").click()
        admin_clients_page.page.get_by_test_id("client_card_name").fill(f"{data_client['name'] + edit_sign}")
        admin_clients_page.client_card.save_client()
        data_client['name'] = data_client['name'] + edit_sign  # В словаре, который создан перед тестом меняем значение
        admin_clients_page.clients.check_new_client(data_client)  # Проверка всех полей нового клиента,
        # в т.ч и изменённое поле

    @staticmethod
    @pytest.mark.smoke
    # @pytest.mark.order(4)
    @allure.title('Удаление записи в справочнике Клиенты')
    @allure.story(jira.JIRA_LINK + 'MDP-1168')
    @allure.testcase(case.ALLURE_LINK + '195067')
    def test_delete_client(
            admin_clients_page: AdminOfficeClientsPage,
            authorization_in_admin_office_with_token,
    ):
        token = authorization_in_admin_office_with_token
        created_client_id = str(get_client_by_naming(data_client['naming']).id)
        admin_clients_page.page.get_by_role('row', name=created_client_id).get_by_role(
            'button').click()
        admin_clients_page.page.get_by_role("button", name="Удалить").click()
        admin_clients_page.page.get_by_test_id("dialog_confirm").click()
        assert get_client_info(created_client_id, token), "Новый клиент почему-то не удалился"
