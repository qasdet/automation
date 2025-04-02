import allure
import pytest

from admin_office.api_interactions.user_candidates.user_candidates_api_interactions import (
    get_list_of_the_user_candidates,
)
from db_stuff.db_interactions.user_candidates_db_interactions import get_list_of_the_user_candidates_from_db
from helper.linkshort import JiraLink as jira


@pytest.mark.usefixtures('authorization_in_admin_office_with_token')
class TestUserCandidateAPI:
    @staticmethod
    @pytest.mark.regress()
    @allure.title('"Получение всех актуальных заявок')
    @allure.story(jira.JIRA_LINK + 'MDP-4444')
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_all_records(authorization_in_admin_office_with_token) -> None:
        """Получение всех актуальных заявок"""
        token = authorization_in_admin_office_with_token
        user_candidates_service = get_list_of_the_user_candidates(token)
        user_candidates_db = get_list_of_the_user_candidates_from_db()
        assert len(user_candidates_db) == len(
            user_candidates_service
        ), 'Количество записей в БД не равно количеству записей с сервиса'
        assert (
            user_candidates_service == user_candidates_db
        ), 'Данные с сервиса не совпадают с данными из БД'
