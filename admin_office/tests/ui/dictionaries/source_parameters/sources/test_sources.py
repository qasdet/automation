import allure
import pytest

from admin_office.components.pages.sources.sources_page import (
    AdminOfficeSourcesPage,
)
from admin_office.constants import LIMIT_OF_ROWS_ON_ONE_PAGE_IN_SOURCES
from admin_office.api_interactions.sources.sources_api_interactions import (
    get_admin_sources,
    get_specific_source_by_id,
)
from helper.names_generator.sources_name_generator import (
    name_generator,
    short_name_generator,
    naming_generator,
    code_generator,
    url_generator,
)
from helper.names_generator.random_latin_letters_generator import generate_random_letters
from db_stuff.db_interactions.sources_db_interactions import (
    get_source_id_by_naming,
    delete_source_by_id,
)
from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira

unique_hash = generate_random_letters(4)
data_source = {
    'name': name_generator(unique_hash),
    'short_name': short_name_generator(unique_hash),
    'naming': naming_generator(unique_hash),
    'url': url_generator(),
    'code': code_generator(unique_hash),
}


@pytest.fixture()
def clean_up_sources_data(
        authorization_in_admin_office_with_token,
):
    """ Удаляет данные после выполнения всех тестов """
    yield
    source_id = get_source_id_by_naming(data_source['naming'])
    if source_id:
        delete_source_by_id(source_id)


@pytest.mark.usefixtures('authorization_in_admin_office_with_token')
class TestSources:
    @staticmethod
    @pytest.mark.smoke
    @allure.title('Просмотр записей в справочнике Площадки')
    @allure.story(jira.JIRA_LINK + 'MDP-1166')
    @allure.testcase(case.ALLURE_LINK + '139743')
    def test_view_sources(
            admin_base_url: str,
            admin_sources_page: AdminOfficeSourcesPage,
            authorization_in_admin_office_with_token: str,
    ):
        token = authorization_in_admin_office_with_token
        admin_sources_page.go_to_sources()
        count_all_rows = len(get_admin_sources(token))
        admin_sources_page.sources.check_quantity_of_sources(count_all_rows)
        admin_sources_page.sources.check_transition_to_next_page(
            count_all_rows
        )
        count_rows_in_second_page = (
            count_all_rows
            if count_all_rows <= LIMIT_OF_ROWS_ON_ONE_PAGE_IN_SOURCES
            else count_all_rows - LIMIT_OF_ROWS_ON_ONE_PAGE_IN_SOURCES
        )
        admin_sources_page.sources.check_quantity_of_sources(
            count_rows_in_second_page
        )
        admin_sources_page.visit(admin_base_url + "/dictionaries/sources")

    @staticmethod
    @pytest.mark.smoke
    @allure.title('Создание записи в справочнике Площадки')
    @allure.story(jira.JIRA_LINK + 'MDP-1166')
    @allure.testcase(case.ALLURE_LINK + '210844')
    def test_create_source(
            admin_base_url: str,
            admin_sources_page: AdminOfficeSourcesPage,
            authorization_in_admin_office_with_token: str,
    ):
        admin_sources_page.visit(admin_base_url + "/dictionaries/sources")
        admin_sources_page.sources.click_create_new_source()
        admin_sources_page.sources_card.sources_fill_all_fields(**data_source)
        admin_sources_page.sources_card.click_sources_button_create()
        created_source_id = str(get_source_id_by_naming(data_source['naming']))
        data_source['id'] = created_source_id
        admin_sources_page.sources.page.reload(wait_until='load')
        admin_sources_page.sources.check_new_source(data_source)

    @staticmethod
    @pytest.mark.smoke
    @allure.title('Редактирование записи через контекстное меню в справочнике площадки')
    @allure.story(jira.JIRA_LINK + 'MDP-1166')
    @allure.testcase(case.ALLURE_LINK + '130885')
    def test_edit_source_context_menu(
            admin_base_url: str,
            admin_sources_page: AdminOfficeSourcesPage,
            authorization_in_admin_office_with_token: str,
    ):
        admin_sources_page.go_to_sources()
        created_source_id = str(get_source_id_by_naming(data_source['naming']))
        admin_sources_page.sources.page.get_by_role('row', name=created_source_id).get_by_role(
            'button').click()
        admin_sources_page.sources.page.get_by_role("button", name="Редактировать").click()
        data_source['name'] = data_source['name'] + 'ed'
        data_source['url'] = 'https://mts.ru'
        admin_sources_page.sources_card.fill_sources_name_field(data_source['name'])
        admin_sources_page.sources_card.fill_sources_url_field(data_source['url'])
        admin_sources_page.sources_card.fill_sources_status_dropdown('Приостановлен')
        admin_sources_page.sources_card.click_sources_button_create()
        admin_sources_page.sources.page.reload(wait_until='load')
        admin_sources_page.sources.check_new_source(data_source)

    @staticmethod
    @pytest.mark.smoke
    @allure.title('Редактировать запись, оставив только обязательные поля')
    @allure.story(jira.JIRA_LINK + 'MDP-1166')
    @allure.testcase(case.ALLURE_LINK + '139775')
    def test_edit_by_leave_mandatory_fields_only(
            admin_base_url: str,
            admin_sources_page: AdminOfficeSourcesPage,
            authorization_in_admin_office_with_token: str,
            clean_up_sources_data,
    ):
        token = authorization_in_admin_office_with_token
        admin_sources_page.go_to_sources()
        created_source_id = str(get_source_id_by_naming(data_source['naming']))
        admin_sources_page.sources.page.get_by_role('row', name=created_source_id).get_by_role(
            'button').click()
        admin_sources_page.sources.page.get_by_role("button", name="Редактировать").click()
        admin_sources_page.sources_card.click_sources_adset_checkbox()
        admin_sources_page.sources_card.click_sources_auto_gather_checkbox()
        admin_sources_page.sources_card.click_sources_sizes_button_delete()
        admin_sources_page.sources_card.click_sources_remove_button_buy_types()
        admin_sources_page.sources_card.click_sources_button_create()
        admin_sources_page.sources.page.reload(wait_until='load')
        admin_sources_page.sources.check_new_source(data_source)
        delete_source_by_id(created_source_id)
        assert not get_specific_source_by_id(created_source_id, token), "Кажется, после теста осталось что-то лишнее"
