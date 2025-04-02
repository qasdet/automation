import allure
import pytest

from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira
from user_office.api_interactions.campaign.campaign_api_interactions import (
    CampaignsMutationsAPI,
)
from user_office.api_interactions.mediaplan.mediaplan_api_interactions import (
    MplanQueriesAPI,
    MplansMutationsAPI,
)


@pytest.mark.usefixtures('authorization_in_user_office_with_token')
class TestMplanAPI:
    @staticmethod
    @pytest.mark.regress()
    @pytest.mark.skip('MDP-6470: Переписать API тест создания черновика МП')
    @allure.title('API тест создания и редактирования черновика медиаплана. Поля заполнены частично')
    @allure.story(jira.JIRA_LINK + 'MDP-5021')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(case.ALLURE_LINK + '368558?treeId=289')
    def test_create_and_update_draft_mplan_part(
        authorization_in_user_office_with_token,
        digital_test_data,
    ):
        token = authorization_in_user_office_with_token
        campaign_id = CampaignsMutationsAPI(token).create_campaign_full(
            digital_test_data
        )
        created_mplan_data = MplansMutationsAPI(token).create_draft_mplan_part(
            campaign_id
        )
        mplan_data = MplanQueriesAPI(token).get_mplan_by_id(
            created_mplan_data['data']['mplanDraftCreate']['id']
        )
        assert (
                created_mplan_data['data']['mplanDraftCreate']
                == mplan_data['data']['mplans'][0]
        )
        updated_mplan_data = MplansMutationsAPI(token).update_draft_mplan(
            campaign_id, created_mplan_data['data']['mplanDraftCreate']['id'], digital_test_data
        )
        new_mplan_data = MplanQueriesAPI(token).get_mplan_by_id(
            created_mplan_data['data']['mplanDraftCreate']['id']
        )
        assert (
                updated_mplan_data['data']['mplanDraftSave']
                == new_mplan_data['data']['mplans'][0]
        )

    @staticmethod
    @pytest.mark.regress()
    @allure.title('API тест создания медиаплана. Статус Планирование')
    @allure.story(jira.JIRA_LINK + 'MDP-6398')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(case.ALLURE_LINK + '368559?treeId=289')
    def test_create_mplan_planning_status(
            authorization_in_user_office_with_token,
            digital_test_data,
    ):
        token = authorization_in_user_office_with_token
        campaign_id = CampaignsMutationsAPI(token).create_campaign_part(
            digital_test_data
        )
        created_mplan_data = MplansMutationsAPI(token).create_mplan_full(
            campaign_id, digital_test_data
        )
        mplan_data = MplanQueriesAPI(token).get_mplan_by_id(
            created_mplan_data['data']['mplanPlanningCreate']['id']
        )
        assert (
                created_mplan_data['data']['mplanPlanningCreate']
                == mplan_data['data']['mplans'][0]
        )

