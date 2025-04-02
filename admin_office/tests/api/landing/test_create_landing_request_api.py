import allure
import pytest

from admin_office.components.pages.user_candidates.user_candidates_page import (
    AdminOfficeUserCandidatesPage,
)
from admin_office.api_interactions.user_candidates.user_candidates_api_interactions import (
    delete_user_candidate_by_id,
    leave_a_request_for_create_user,
)
from admin_office.tests.api.landing.data_make_for_user_candidates import (
    make_data_all_user_candidate_fields,
)
from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira

user_candidate_data = make_data_all_user_candidate_fields('Иван',
                                                          'Апишный',
                                                          'ООО АПИ-Автотесты',
                                                          'Эта заявка создана автоматическим тестом через API')


@pytest.mark.usefixtures('authorization_in_admin_office_with_token')
class TestUserCandidatesAPI:
    @staticmethod
    @pytest.mark.smoke
    @allure.title('Справочник Заявки')
    @allure.story(
        jira.JIRA_LINK + 'MDP-2059'
    )  # Не нашёл задачу про справочник заявок. Добавил примерно подходящую
    @allure.testcase(case.ALLURE_LINK + '155526')
    def test_create_user_candidate_request_api(
        admin_user_candidates_page: AdminOfficeUserCandidatesPage,
        authorization_in_admin_office_with_token,
    ):
        token = authorization_in_admin_office_with_token
        user_candidate = leave_a_request_for_create_user(**user_candidate_data)
        user_candidate_data['id'] = user_candidate['id']
        admin_user_candidates_page.side_bar.goto('Заявки')
        admin_user_candidates_page.user_candidates.check_new_user_candidate(
            user_candidate_data
        )
        delete_user_candidate_by_id(user_candidate_data['id'], token)
