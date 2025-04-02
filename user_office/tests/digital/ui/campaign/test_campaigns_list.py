import allure
import pytest

from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira
from user_office.components.pages.campaigns.campaigns_list_page import CampaignsListPage
from user_office.components.pages.campaigns.campaign_page import CampaignPage
from db_stuff.db_interactions.campaigns_db_interactions import get_campaigns_for_campaigns_list
from db_stuff.db_interactions.organizations_db_interactions import get_organization_by_email
from user_office.api_interactions.campaign.campaign_api_interactions import CampaignsMutationsAPI
from user_office.constants import EMAIL_ORGANIZATION


@pytest.mark.usefixtures('authorization_in_user_office_with_token')
class TestCampaignsList:
    @staticmethod
    @allure.title(test_title='Верификация страницы списка кампаний и проверка элементов списка')
    @allure.severity(severity_level=allure.severity_level.CRITICAL)
    @allure.issue(jira.JIRA_LINK + 'MDP-5138')
    @allure.testcase(case.ALLURE_LINK + '121241?treeId=289')
    @pytest.mark.regress
    @pytest.mark.skip('MDP-6635: UI / Regress / Переделать проверку списка кампаний в тесте test_campaigns_list.py')
    def test_campaigns_list(
            campaigns_list_page: CampaignsListPage,
            office_base_url: str,
    ) -> None:

        campaigns_list_page.visit(office_base_url)
        organization_id = get_organization_by_email(EMAIL_ORGANIZATION).id
        campaigns_data = get_campaigns_for_campaigns_list(organization_id)
        campaigns_list_page.digital_campaigns_list.check_campaigns_list_elements()
        campaigns_list_page.digital_campaigns_list.check_campaigns_list(campaigns_data)

    @staticmethod
    @allure.title(test_title='Тест отображения ко брендов в списке кампаний и на странице кампании')
    @allure.severity(severity_level=allure.severity_level.CRITICAL)
    @allure.issue(jira.JIRA_LINK + 'MDP-5138')
    @allure.testcase(case.ALLURE_LINK + '320154?treeId=289')
    @pytest.mark.regress
    def test_campaign_with_co_brand_in_campaigns_list(
            authorization_in_user_office_with_token,
            campaigns_list_page: CampaignsListPage,
            campaign_page: CampaignPage,
            digital_test_data,
            office_base_url: str
    ) -> None:
        CampaignsMutationsAPI(authorization_in_user_office_with_token).create_campaign_part_with_two_co_brands(
            digital_test_data
        )
        campaigns_list_page.visit(office_base_url)
        campaigns_list_page.digital_campaigns_list.check_created_campaign_with_two_co_brands_in_campaign_list(
            digital_test_data
        )
        campaigns_list_page.digital_campaigns_list.open_campaign(digital_test_data['campaign_name'])
        campaign_page.digital_campaign.check_co_brands_in_campaign_page(digital_test_data)


