import allure
import pytest

from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira
from user_office.components.pages.authorization.authorization_page import (
    AuthorizationPage,
)
from user_office.components.pages.health_check.health_check_page import (
    HealthCheckPage,
)


class TestHealth:
    @allure.title(test_title='Здоровье юзер офиса')
    @allure.severity(severity_level=allure.severity_level.CRITICAL)
    @allure.issue(jira.JIRA_LINK + 'MDP-3749')
    @allure.testcase(case.ALLURE_LINK + '12383489')
    @pytest.mark.health_check
    def test_health_user_office(
        self,
        user_office_authorization: AuthorizationPage,
        health_check_page: HealthCheckPage,
        office_base_url: str,
    ) -> None:
        user_office_authorization.visit(url=office_base_url)
        user_office_authorization.authorize.auth_user_office()
        health_check_page.health_user_office.check_all_text()
