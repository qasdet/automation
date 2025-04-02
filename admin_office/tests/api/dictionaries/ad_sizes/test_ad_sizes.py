import allure
import pytest

from db_stuff.db_interactions.ad_sizes_db_interactions import get_list_of_the_ad_sizes_from_db
from helper.array_helper import compare_the_response_from_service_with_expected_response
from admin_office.api_interactions.ad_sizes.ad_sizes_api_interactions import get_list_of_the_ad_sizes
from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira


@pytest.mark.usefixtures('authorization_in_admin_office_with_token')
class TestAdSizeAPI:
    @staticmethod
    @pytest.mark.regress()
    @allure.title('Получение списка рекламных размеров через API')
    @allure.story(jira.JIRA_LINK + 'MDP-531')
    @allure.testcase(case.ALLURE_LINK + '153257')
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_all_records(authorization_in_admin_office_with_token) -> None:
        """Получение всех записей"""
        token = authorization_in_admin_office_with_token
        ad_sizes_service = get_list_of_the_ad_sizes(token)
        ad_sizes_db = get_list_of_the_ad_sizes_from_db()
        assert (
            ad_sizes_service == ad_sizes_db
        ), 'Данные с сервиса не совпадают с данными из БД'

    @staticmethod
    @pytest.mark.regress()
    @allure.title('Получение рекламного размера через API')
    @allure.story(jira.JIRA_LINK + 'MDP-531')
    @allure.testcase(case.ALLURE_LINK + '153258')
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_one_records(authorization_in_admin_office_with_token) -> None:
        """Получение записи по id"""
        token = authorization_in_admin_office_with_token
        ad_sizes_db = get_list_of_the_ad_sizes_from_db()
        ad_size_service = get_list_of_the_ad_sizes(
            token=token, variables={'id': ad_sizes_db[0]['id']}
        )
        compare_the_response_from_service_with_expected_response(
            ad_size_service[0], ad_sizes_db[0]
        )
