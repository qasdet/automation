import allure
import pytest

from admin_office.components.pages.authorization.authorization_page import (
    AdminOfficeAuthorizationPage,
)
from admin_office.components.pages.home.home_page import AdminOfficeHomePage
from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira


class TestHealth:
    @staticmethod
    @allure.title('Здоровье админ офиса')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.story(jira.JIRA_LINK + 'MDP-3019')
    @allure.testcase(case.ALLURE_LINK + '124081')
    @pytest.mark.health_check
    def test_health_admin_office(
        admin_office_authorization: AdminOfficeAuthorizationPage,
        admin_home_page: AdminOfficeHomePage,
        admin_base_url: str,
    ):
        admin_office_authorization.visit(admin_base_url)
        admin_office_authorization.authorization.auth_admin_office()
        admin_home_page.side_bar.check_all_text()
