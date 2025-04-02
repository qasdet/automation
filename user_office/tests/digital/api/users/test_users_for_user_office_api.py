import allure
import pytest

from db_stuff.db_interactions.organizations_db_interactions import (
    get_organization_by_email,
)
from helper.linkshort import JiraLink as jira
from db_stuff.db_interactions.users_db_interactions import united_list_users_and_persons_by_organization_id
from user_office.api_interactions.users.users_api_interactions import UsersQueriesAPI
from user_office.constants import EMAIL_ORGANIZATION


@pytest.mark.usefixtures('authorization_in_user_office_with_token')
class TestUsers:
    @staticmethod
    @pytest.mark.regress()
    @allure.title('Получение списка пользователей через API у организации')
    @allure.story(jira.JIRA_LINK + 'MDP-4142')
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_list_users_for_organization(
        authorization_in_user_office_with_token,
    ):
        token = authorization_in_user_office_with_token
        organization = get_organization_by_email(EMAIL_ORGANIZATION)
        users_for_organization_db = united_list_users_and_persons_by_organization_id(
            organization.id
        )
        users_for_organization_db.sort(
            key=lambda dictionary: dictionary['login']
        )
        users_for_organization_api = UsersQueriesAPI(
                token
            ).get_all_list_users()
        users_for_organization_api.sort(
            key=lambda dictionary: dictionary['login']
        )
        assert (
            users_for_organization_api == users_for_organization_db
        ), 'Список пользователей через API не совпадает с ожидаемым из БД'
