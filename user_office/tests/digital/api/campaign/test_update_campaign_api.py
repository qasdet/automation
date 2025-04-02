import allure
import pytest

from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira
from user_office.api_interactions.campaign.campaign_api_interactions import (
    CampaignsMutationsAPI,
    CampaignsQueriesAPI,
)


@pytest.mark.usefixtures('authorization_in_user_office_with_token')
class TestUpdateCampaignAPI:
    @staticmethod
    @pytest.mark.regress()
    @allure.title('API тест создания и редактирования черновика кампании')
    @allure.story(jira.JIRA_LINK + 'MDP-4454')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(case.ALLURE_LINK + '215682?treeId=289')
    def test_create_and_update_draft_campaign(
        authorization_in_user_office_with_token,
        digital_test_data,
    ):
        token = authorization_in_user_office_with_token
        draft_campaign_id = CampaignsMutationsAPI(token).create_draft_campaign_part(
            digital_test_data
        )
        campaign_data = CampaignsQueriesAPI(token).get_campaign_by_id(
            draft_campaign_id
        )
        assert (
                campaign_data['data']['campaigns'][0]['name']
                == digital_test_data['campaign_name']
        )
        assert (
                campaign_data['data']['campaigns'][0]['code']
                == digital_test_data['campaign_naming']
        )
        assert (
            campaign_data['data']['campaigns'][0]['status']['name']
            == 'Черновик'
        )
        updated_campaign_data = CampaignsMutationsAPI(token).update_campaign_part(
            draft_campaign_id, digital_test_data
        )
        new_campaign_data = CampaignsQueriesAPI(token).get_campaign_by_id(
            draft_campaign_id
        )
        assert (
            new_campaign_data['data']['campaigns'][0]
            == updated_campaign_data["data"]["campaignUpdate"]
        )

    @staticmethod
    @pytest.mark.regress()
    @allure.title(
        'API тест создания и редактирования кампании. Частично заполненые поля'
    )
    @allure.story(jira.JIRA_LINK + 'MDP-4455')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(case.ALLURE_LINK + '215680?treeId=289')
    def test_create_and_update_campaign_part(
        authorization_in_user_office_with_token,
        digital_test_data,
    ):
        token = authorization_in_user_office_with_token
        campaign_id = CampaignsMutationsAPI(token).create_campaign_part(
            digital_test_data
        )
        campaign_data = CampaignsQueriesAPI(token).get_campaign_by_id(
            campaign_id
        )
        assert (
                campaign_data['data']['campaigns'][0]['name']
                == digital_test_data['campaign_name']
        )
        assert (
                campaign_data['data']['campaigns'][0]['code']
                == digital_test_data['campaign_naming']
        )
        assert (
            campaign_data['data']['campaigns'][0]['status']['name']
            == 'Планирование'
        )
        updated_campaign_data = CampaignsMutationsAPI(token).update_campaign_part(
            campaign_id, digital_test_data
        )
        new_campaign_data = CampaignsQueriesAPI(token).get_campaign_by_id(
            campaign_id
        )
        assert (
            new_campaign_data['data']['campaigns'][0]
            == updated_campaign_data["data"]["campaignUpdate"],
        )

    @staticmethod
    @pytest.mark.regress()
    @allure.title(
        'API тест создания и редактирования кампании. Все поля заполнены'
    )
    @allure.story(jira.JIRA_LINK + 'MDP-4455')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(case.ALLURE_LINK + '215680?treeId=289')
    def test_create_and_update_campaign_full(
        authorization_in_user_office_with_token,
        digital_test_data,
    ):
        token = authorization_in_user_office_with_token
        campaign_id = CampaignsMutationsAPI(token).create_campaign_full(
            digital_test_data
        )
        campaign_data = CampaignsQueriesAPI(token).get_campaign_by_id(
            campaign_id
        )
        assert (
                campaign_data['data']['campaigns'][0]['name']
                == digital_test_data['campaign_name']
        )
        assert (
                campaign_data['data']['campaigns'][0]['code']
                == digital_test_data['campaign_naming']
        )
        assert (
            campaign_data['data']['campaigns'][0]['status']['name']
            == 'Планирование'
        )
        updated_campaign_data = CampaignsMutationsAPI(token).update_campaign_full(
            campaign_id, digital_test_data
        )
        new_campaign_data = CampaignsQueriesAPI(token).get_campaign_by_id(
            campaign_id
        )
        assert (
            new_campaign_data['data']['campaigns'][0]
            == updated_campaign_data["data"]["campaignUpdate"],
        )
