import allure
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

from admin_office.components.pages.authorization.authorization_page import (
    AdminOfficeAuthorizationPage,
)
from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira

disable_warnings(InsecureRequestWarning)


class TestAuthAdminOffice:
    @allure.title('Авторизация в Админ Офисе')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story(jira.JIRA_LINK + 'MDP-341')
    @allure.testcase(case.ALLURE_LINK + '325415')
    def test_auth_admin_office(
        self,
        admin_office_authorization: AdminOfficeAuthorizationPage,
        admin_base_url: str,
    ):
        admin_office_authorization.visit(admin_base_url)
        admin_office_authorization.authorization.auth_admin_office()
