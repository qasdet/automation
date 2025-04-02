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


@pytest.mark.usefixtures('authorization_in_user_office_with_token')
class TestCampaignCreate:
    @staticmethod
    @pytest.mark.regress()
    @allure.title('Создание черновика. Все поля заполнены')
    @allure.story(jira.JIRA_LINK + 'MDP-3436')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(case.ALLURE_LINK + '121240?treeId=289')
    def test_create_draft_full(
            campaign_page: CampaignPage,
            campaigns_list_page: CampaignsListPage,
            create_campaign_page: CreateCampaignPage,
            about_campaign_page: AboutCampaignPage,
            digital_test_data,
            office_base_url: str,
    ):
        campaigns_list_page.visit(office_base_url)
        campaigns_list_page.digital_campaigns_list.click_create_campaign_button()
        create_campaign_page.digital_create_campaign.create_draft_campaign_full(
            digital_test_data
        )
        campaign_page.digital_campaign.open_digital_campaigns_list()
        campaigns_list_page.digital_campaigns_list.open_campaign(
            digital_test_data['campaign_name']
        )
        about_campaign_page.digital_about_campaign.check_created_draft_campaign_full(
            digital_test_data['campaign_name'], digital_test_data['campaign_naming']
        )

    @staticmethod
    @pytest.mark.regress()
    @allure.title('Создание черновика. Заполнены только обязательные поля')
    @allure.story(jira.JIRA_LINK + 'MDP-2587')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(case.ALLURE_LINK + '122511?treeId=289')
    def test_create_draft_part(
            campaign_page: CampaignPage,
            campaigns_list_page: CampaignsListPage,
            create_campaign_page: CreateCampaignPage,
            about_campaign_page: AboutCampaignPage,
            digital_test_data,
            office_base_url: str,
    ):
        campaigns_list_page.visit(office_base_url)
        campaigns_list_page.digital_campaigns_list.click_create_campaign_button()
        create_campaign_page.digital_create_campaign.create_draft_campaign_part(
            digital_test_data
        )
        campaign_page.digital_campaign.open_digital_campaigns_list()
        campaigns_list_page.digital_campaigns_list.open_campaign(
            digital_test_data['campaign_name']
        )
        about_campaign_page.digital_about_campaign.check_created_draft_campaign_part(
            digital_test_data['campaign_name'], digital_test_data['campaign_naming']
        )

    @staticmethod
    @pytest.mark.smoke()
    @allure.title('Создание кампании. Все поля заполнены')
    @allure.story(jira.JIRA_LINK + 'MDP-2974')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(case.ALLURE_LINK + '122489?treeId=289')
    def test_create_campaign_full(
            campaign_page: CampaignPage,
            campaigns_list_page: CampaignsListPage,
            create_campaign_page: CreateCampaignPage,
            about_campaign_page: AboutCampaignPage,
            digital_test_data,
            office_base_url: str,
    ):
        campaigns_list_page.visit(office_base_url)
        campaigns_list_page.digital_campaigns_list.click_create_campaign_button()
        create_campaign_page.digital_create_campaign.create_campaign_full(
            digital_test_data
        )
        campaign_page.digital_campaign.open_digital_campaigns_list()
        campaigns_list_page.digital_campaigns_list.open_campaign(
            digital_test_data['campaign_name']
        )
        campaign_page.digital_campaign.check_created_campaign_in_campaign_page(digital_test_data)
        campaign_page.digital_campaign.open_about_campaign()
        about_campaign_page.digital_about_campaign.check_created_campaign_full(
            digital_test_data['campaign_name'], digital_test_data['campaign_naming']
        )

    @staticmethod
    @pytest.mark.regress()
    @allure.title('Создание кампании. Заполнены только обязательные поля')
    @allure.story(jira.JIRA_LINK + 'MDP-2587')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(case.ALLURE_LINK + '122502?treeId=289')
    def test_create_campaign_part(
            campaign_page: CampaignPage,
            campaigns_list_page: CampaignsListPage,
            create_campaign_page: CreateCampaignPage,
            about_campaign_page: AboutCampaignPage,
            digital_test_data,
            office_base_url: str,
    ):
        campaigns_list_page.visit(office_base_url)
        campaigns_list_page.digital_campaigns_list.click_create_campaign_button()
        create_campaign_page.digital_create_campaign.create_campaign_part(
            digital_test_data
        )
        campaign_page.digital_campaign.open_digital_campaigns_list()
        campaigns_list_page.digital_campaigns_list.open_campaign(
            digital_test_data['campaign_name']
        )
        campaign_page.digital_campaign.check_created_campaign_in_campaign_page(digital_test_data)
        campaign_page.digital_campaign.open_about_campaign()
        about_campaign_page.digital_about_campaign.check_created_campaign_part(
            digital_test_data['campaign_name'], digital_test_data['campaign_naming']
        )
