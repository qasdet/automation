import allure
import pytest

from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira
from helper.url_constructor import DigitalUrl
from user_office.components.pages.dictionaries.dictionaries_page import (
    DictionariesPage
)


@pytest.mark.usefixtures('authorization_in_user_office_with_token')
class TestVerifyPagesGuides:
    @staticmethod
    @allure.title(test_title='Тест проверки справочников Digital кампании')
    @allure.severity(severity_level=allure.severity_level.CRITICAL)
    @allure.issue(jira.JIRA_LINK + 'MDP-5086')
    @allure.testcase(case.ALLURE_LINK + '435588?treeId=289')
    @pytest.mark.smoke
    def test_dictionaries_digital(
            dictionaries: DictionariesPage,
            office_base_url: str,
    ) -> None:
        url = DigitalUrl.get_url_dictionaries_page(
            office_base_url,
            naming='/naming/'
        )
        dictionaries.visit(url)
        dictionaries.dictionaries_page.check_digital_dict()
