import allure
import pytest

from admin_office.api_interactions.placement_statuses.placement_statuses_api_interactions import (
    get_list_of_the_placement_statuses,
)
from db_stuff.db_interactions.placement_statuses_db_interactions import get_list_of_the_placement_statuses_from_db
from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira


@pytest.mark.usefixtures('authorization_in_admin_office_with_token')
class TestsPlacementStatusesAPI:
    @staticmethod
    @pytest.mark.regress()
    @allure.title('Получение всех записей')
    @allure.story(jira.JIRA_LINK + 'MDP-903')
    @allure.testcase(case.ALLURE_LINK + '149519')
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_all_records(authorization_in_admin_office_with_token) -> None:
        """Получение всех записей"""
        token = authorization_in_admin_office_with_token
        placement_statuses_service = get_list_of_the_placement_statuses(token)
        placement_statuses_service.sort(
            key=lambda dictionary: dictionary['code']
        )
        placement_statuses_db = get_list_of_the_placement_statuses_from_db()
        placement_statuses_db.sort(key=lambda dictionary: dictionary['code'])
        assert (
                placement_statuses_service == placement_statuses_db
        ), 'Данные с сервиса не совпадают с данными из БД'
