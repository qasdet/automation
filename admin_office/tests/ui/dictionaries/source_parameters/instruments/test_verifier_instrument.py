import allure
import pytest

from admin_office.components.pages.instruments.instruments_page import (
    AdminOfficeInstrumentsPage,
)
from db_stuff.db_interactions.sources_db_interactions import (
    get_source_id_by_naming,
    delete_source_by_id,
)
from helper.names_generator.instruments_names_generator import (
    tools_name_generator,
    tools_naming_generator,
    tools_code_generator,
    tools_url_generator,
    tools_short_name_generator,
)
from helper.names_generator.random_latin_letters_generator import generate_random_letters
from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira

unique_hash = generate_random_letters(4)
data_instruments_card = {
    'name': tools_name_generator(unique_hash),
    'short_name': tools_short_name_generator(unique_hash),
    'naming': tools_naming_generator(unique_hash),
    'url': tools_url_generator(),
    'code': tools_code_generator(unique_hash),
}


@pytest.fixture()
def clean_up_verifier_data(
        authorization_in_admin_office_with_token,
):
    """ Удаляет данные после выполнения всех тестов на вкладке 'Верификатор' """
    verifier_id = get_source_id_by_naming(data_instruments_card['naming'])
    if verifier_id:
        delete_source_by_id(verifier_id)


@pytest.mark.usefixtures('authorization_in_admin_office_with_token')
class TestVerifier:
    @staticmethod
    @pytest.mark.smoke
    @allure.title("Создание записи в справочнике 'Инструменты'. Вкладка 'Верификатор'")
    @allure.story(jira.JIRA_LINK + 'MDP-1166')
    @allure.testcase(case.ALLURE_LINK + '211165')
    def test_create_verifier(
            admin_base_url: str,
            admin_instruments_page: AdminOfficeInstrumentsPage,
            authorization_in_admin_office_with_token: str,
    ):
        admin_instruments_page.go_to_instruments()
        admin_instruments_page.instruments.click_verifier_tab()
        admin_instruments_page.instruments.click_tools_button_create()
        admin_instruments_page.instruments_card.fill_tools_type_dropdown('Верификатор')
        admin_instruments_page.instruments_card.fill_tools_code_field(data_instruments_card['code'])
        admin_instruments_page.instruments_card.click_tools_can_auto_gather_switch()
        admin_instruments_page.instruments_card.fill_tools_name_field(data_instruments_card['name'])
        admin_instruments_page.instruments_card.fill_tools_short_name_field(data_instruments_card['short_name'])
        admin_instruments_page.instruments_card.fill_tools_url_field(data_instruments_card['url'])
        admin_instruments_page.instruments_card.fill_tools_naming_field(data_instruments_card['naming'])
        admin_instruments_page.instruments_card.fill_tools_status_dropdown()
        admin_instruments_page.instruments_card.click_create_button()
        admin_instruments_page.instruments.page.reload(wait_until='load')
        instrument_id = get_source_id_by_naming(data_instruments_card['naming'])
        data_instruments_card['id'] = str(instrument_id)
        admin_instruments_page.instruments.check_instruments_table(data_instruments_card)

    @staticmethod
    @pytest.mark.smoke
    @allure.title("Редактирование записи в справочнике 'Инструменты'. Вкладка 'Верификатор'")
    @allure.story(jira.JIRA_LINK + 'MDP-1166')
    @allure.testcase(case.ALLURE_LINK + '131397')
    def test_edit_verifier(
            admin_base_url: str,
            admin_instruments_page: AdminOfficeInstrumentsPage,
            authorization_in_admin_office_with_token: str,
    ):
        created_verifier_id = str(get_source_id_by_naming(data_instruments_card['naming']))
        admin_instruments_page.instruments.page.get_by_role('row', name=created_verifier_id).get_by_role(
            'link').click()
        data_instruments_card['name'] = data_instruments_card['name'] + 'ed'
        data_instruments_card['url'] = 'https://mts.ru'
        admin_instruments_page.instruments_card.fill_tools_name_field(data_instruments_card['name'])
        admin_instruments_page.instruments_card.fill_tools_url_field(data_instruments_card['url'])
        admin_instruments_page.instruments_card.click_tools_can_auto_gather_switch()
        admin_instruments_page.instruments_card.fill_tools_status_dropdown('Приостановлен')
        admin_instruments_page.instruments_card.click_create_button()
        admin_instruments_page.instruments.page.reload(wait_until='load')
        admin_instruments_page.instruments.check_instruments_table(data_instruments_card)

    @staticmethod
    @pytest.mark.smoke
    @allure.title("Редактирование через контекстное меню записи в справочнике 'Инструменты'. Вкладка 'Верификатор'")
    @allure.story(jira.JIRA_LINK + 'MDP-1166')
    @allure.testcase(case.ALLURE_LINK + '131398')
    def test_edit_verifier_context_menu(
            admin_base_url: str,
            admin_instruments_page: AdminOfficeInstrumentsPage,
            authorization_in_admin_office_with_token: str,
            clean_up_verifier_data,
    ):
        created_verifier_id = str(get_source_id_by_naming(data_instruments_card['naming']))
        admin_instruments_page.instruments.page.get_by_role('row', name=created_verifier_id).get_by_role(
            'button').click()
        admin_instruments_page.instruments.page.get_by_role("button", name="Редактировать").click()
        data_instruments_card['name'] = data_instruments_card['name'] + 'eded'
        data_instruments_card['url'] = 'https://example.com'
        admin_instruments_page.instruments_card.fill_tools_name_field(data_instruments_card['name'])
        admin_instruments_page.instruments_card.fill_tools_url_field(data_instruments_card['url'])
        admin_instruments_page.instruments_card.click_tools_can_auto_gather_switch()
        admin_instruments_page.instruments_card.fill_tools_status_dropdown('Удален')
        admin_instruments_page.instruments_card.click_create_button()
        admin_instruments_page.instruments.page.reload(wait_until='load')
        admin_instruments_page.instruments.check_instruments_table(data_instruments_card)
        delete_source_by_id(created_verifier_id)
