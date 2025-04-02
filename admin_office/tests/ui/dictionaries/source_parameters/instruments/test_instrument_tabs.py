import allure
import pytest

from admin_office.components.pages.instruments.instruments_page import (
    AdminOfficeInstrumentsPage,
)
from admin_office.api_interactions.instruments.instruments_api_interactions import get_admin_instruments
from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira


@pytest.mark.usefixtures('authorization_in_admin_office_with_token')
class TestInstruments:
    @staticmethod
    @pytest.mark.smoke
    @allure.title('Просмотр записей в справочнике Инструменты')
    @allure.story(jira.JIRA_LINK + 'MDP-1166')
    @allure.testcase(case.ALLURE_LINK + '131399')
    def test_view_instruments(
            admin_base_url: str,
            admin_instruments_page: AdminOfficeInstrumentsPage,
            authorization_in_admin_office_with_token: str,
    ):
        token = authorization_in_admin_office_with_token
        admin_instruments_page.go_to_instruments()

        list_of_verificators = get_admin_instruments(token, 'VERIFIER')
        admin_instruments_page.instruments.click_verifier_tab()
        for item in list_of_verificators:
            admin_instruments_page.instruments.check_instruments_table(item)

        list_of_postclicks = get_admin_instruments(token, 'POSTCLICK')
        admin_instruments_page.instruments.click_postclick_tab()
        for item in list_of_postclicks:
            admin_instruments_page.instruments.check_instruments_table(item)

        list_of_trackers = get_admin_instruments(token, 'TRACKER')
        admin_instruments_page.instruments.click_tracker_tab()
        for item in list_of_trackers:
            admin_instruments_page.instruments.check_instruments_table(item)
