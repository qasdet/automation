import allure
import pytest

from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira

from user_office.components.pages.campaigns.about_campaign_page import (
    AboutCampaignPage,
)
from user_office.components.pages.campaigns.campaign_page import CampaignPage
from user_office.components.pages.campaigns.campaigns_list_page import (
    CampaignsListPage,
)
from user_office.components.pages.campaigns.create_campaign_page import (
    CreateCampaignPage,
)
from user_office.api_interactions.campaign.campaign_api_interactions import CampaignsMutationsAPI
from helper.url_constructor import DigitalUrl


@pytest.mark.usefixtures('authorization_in_user_office_with_token')
class TestRetryCampaign:
    @staticmethod
    @pytest.mark.regress()
    @allure.title('Повтор черновика кампании')
    @allure.story(jira.JIRA_LINK + 'MDP-3502')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(case.ALLURE_LINK + '280743?treeId=289')
    def test_retry_draft_campaign(
        campaign_page: CampaignPage,
        campaigns_list_page: CampaignsListPage,
        create_campaign_page: CreateCampaignPage,
        about_campaign_page: AboutCampaignPage,
        digital_test_data,
        authorization_in_user_office_with_token,
        office_base_url: str,
    ):
        CampaignsMutationsAPI(authorization_in_user_office_with_token).create_draft_campaign_part(
            digital_test_data
        )
        campaigns_list_page.visit(DigitalUrl.get_url_digital_campaigns_list_page(office_base_url))
        campaigns_list_page.digital_campaigns_list.retry_campaign(
            digital_test_data['campaign_naming']
        )
        create_campaign_page.digital_create_campaign.update_data_and_save_draft(
            digital_test_data
        )
        campaign_page.digital_campaign.open_digital_campaigns_list()
        campaigns_list_page.digital_campaigns_list.open_campaign(
            digital_test_data['new_campaign_name']
        )
        about_campaign_page.digital_about_campaign.check_created_draft_campaign_part(
            digital_test_data['new_campaign_name'], digital_test_data['new_campaign_naming']
        )

    @staticmethod
    @pytest.mark.regress()
    @allure.title('Повтор кампании')
    @allure.story(jira.JIRA_LINK + 'MDP-3504')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(case.ALLURE_LINK + '157877?treeId=289')
    def test_retry_campaign(
        campaign_page: CampaignPage,
        campaigns_list_page: CampaignsListPage,
        create_campaign_page: CreateCampaignPage,
        about_campaign_page: AboutCampaignPage,
        digital_test_data,
        authorization_in_user_office_with_token,
        office_base_url: str,
    ):
        CampaignsMutationsAPI(authorization_in_user_office_with_token).create_campaign_full(
            digital_test_data
        )
        campaigns_list_page.visit(DigitalUrl.get_url_digital_campaigns_list_page(office_base_url))
        campaigns_list_page.digital_campaigns_list.retry_campaign(
            digital_test_data['campaign_naming']
        )
        create_campaign_page.digital_create_campaign.update_data_and_save_campaign(
            digital_test_data
        )
        campaign_page.digital_campaign.open_digital_campaigns_list()
        campaigns_list_page.digital_campaigns_list.open_campaign(
            digital_test_data['new_campaign_name']
        )
        campaign_page.digital_campaign.check_created_campaign_in_campaign_page(
            digital_test_data['new_campaign_name'], digital_test_data['new_campaign_naming']
        )
        campaign_page.digital_campaign.open_about_campaign()
        about_campaign_page.digital_about_campaign.check_created_campaign_part(
            digital_test_data['new_campaign_name'], digital_test_data['new_campaign_naming']
        )
