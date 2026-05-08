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
    """
    Набор тестов для проверки функциональности справочника Клиенты.

    Тестирует основные сценарии:
    - Просмотр списка клиентов с пагинацией
    - Создание нового клиента
    - Редактирование клиента
    - Удаление клиента
    """

    @staticmethod
    @pytest.mark.smoke
    @allure.title('Справочник Клиенты')
    @allure.story(jira.JIRA_LINK + 'MDP-1168')
    @allure.testcase(case.ALLURE_LINK + '195066')
    def test_view_clients(
            admin_base_url: str,
            admin_clients_page: AdminOfficeClientsPage,
            authorization_in_admin_office_with_token: str,
    ):
        """
        Тест проверки отображения справочника клиентов с пагинацией.

        Проверяет:
        - Общее количество клиентов соответствует API
        - Пагинация корректно работает при переходе на вторую страницу
        - Количество строк на второй странице соответствует ожиданиям
        """
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

    @staticmethod
    @pytest.mark.smoke
    @allure.title('Создание записи в справочнике Клиенты')
    @allure.story(jira.JIRA_LINK + 'MDP-1168')
    @allure.testcase(case.ALLURE_LINK + '195067')
    def test_create_client(
            admin_clients_page: AdminOfficeClientsPage,
            authorization_in_admin_office_with_token,
    ):
        """
        Тест создания нового клиента с заполнением всех полей.

        Проверяет полный цикл создания клиента:
        - Открытие формы создания
        - Заполнение всех полей данными
        - Сохранение клиента
        - Проверка отображения созданного клиента в списке
        """
        admin_clients_page.go_to_clients()
        admin_clients_page.clients.open_the_client_creation_form()
        admin_clients_page.client_card.fill_all_fields(**data_client)
        admin_clients_page.client_card.save_client()
        admin_clients_page.clients.check_new_client(data_client)

    @staticmethod
    @pytest.mark.smoke
    @allure.title('Редактирование записи в справочнике Клиенты')
    @allure.story(jira.JIRA_LINK + 'MDP-1168')
    @allure.testcase(case.ALLURE_LINK + '195067')
    def test_edit_client(
            admin_clients_page: AdminOfficeClientsPage,
    ):
        """
        Тест редактирования клиента.

        Проверяет:
        - Открытие формы редактирования через меню строки
        - Изменение названия клиента
        - Сохранение изменений
        - Проверка что данные обновились
        """
        created_client_id = str(get_client_by_naming(data_client['naming']).id)
        admin_clients_page.clients.table.open_menu_action_in_row_by_contains_text(created_client_id)
        admin_clients_page.clients.table.click_item_menu_action('Редактировать')
        admin_clients_page.client_card.input_name.click()
        admin_clients_page.client_card.input_name.fill(f"{data_client['name'] + edit_sign}")
        admin_clients_page.client_card.save_client()
        data_client['name'] = data_client['name'] + edit_sign
        admin_clients_page.clients.check_new_client(data_client)

    @staticmethod
    @pytest.mark.smoke
    @allure.title('Удаление записи в справочнике Клиенты')
    @allure.story(jira.JIRA_LINK + 'MDP-1168')
    @allure.testcase(case.ALLURE_LINK + '195067')
    def test_delete_client(
            admin_clients_page: AdminOfficeClientsPage,
            authorization_in_admin_office_with_token,
    ):
        """
        Тест удаления клиента.

        Проверяет:
        - Открытие контекстного меню строки
        - Удаление клиента через кнопку "Удалить"
        - Подтверждение удаления в диалоге
        - Проверка что клиент больше не отображается в списке
        """
        token = authorization_in_admin_office_with_token
        created_client_id = str(get_client_by_naming(data_client['naming']).id)
        admin_clients_page.clients.table.open_menu_action_in_row_by_contains_text(created_client_id)
        admin_clients_page.clients.table.click_item_menu_action('Удалить')
        admin_clients_page.confirmation_dialog.confirm()
        admin_clients_page.clients.table.row_by_contains_text(created_client_id).should_not_be_visible()
        assert get_client_info(created_client_id, token), "Клиент не был удален"
