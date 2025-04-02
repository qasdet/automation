import allure
import pytest

from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira
from user_office.components.pages.mediaplan.mediaplan_page import MediaplanPage
from user_office.api_interactions.campaign.campaign_api_interactions import CampaignsMutationsAPI
from user_office.api_interactions.mediaplan.mediaplan_api_interactions import MplansMutationsAPI
from user_office.api_interactions.placement.placement_api_interactions import PlacementMutationsAPI, PlacementQueriesAPI
from user_office.api_interactions.targeting.targeting_api_interactions import TargetingMutationsAPI
from helper.url_constructor import DigitalUrl


@pytest.mark.usefixtures('authorization_in_user_office_with_token')
class TestMplanAnalytics:
    @staticmethod
    @pytest.mark.smoke()
    @allure.title("Тест проверки вкладки Аналитика на странице медиаплана. Статус Планирование")
    @allure.story(jira.JIRA_LINK + 'MDP-4962')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(case.ALLURE_LINK + '335384?treeId=289')
    def test_mplan_analytics_tab_planning_status(
        mediaplan_page: MediaplanPage,
        digital_test_data,
        authorization_in_user_office_with_token,
        office_base_url: str,
    ):
        campaign_data = CampaignsMutationsAPI(authorization_in_user_office_with_token).create_campaign_part_with_budget(
            digital_test_data
        )
        mplan_data = MplansMutationsAPI(authorization_in_user_office_with_token).create_mplan_part(
            campaign_data['data']['campaignCreate']['id']
        )
        mediaplan_page.visit(DigitalUrl.get_url_digital_mplan_page(
            office_base_url, mplan_data['data']['mplanPlanningCreate']['id']
            )
        )
        campaign_budget = campaign_data['data']['campaignCreate']['budget']
        mediaplan_page.digital_mediaplan.open_analytics_tab()
        mediaplan_page.digital_mediaplan_analytics.check_analytics_page_planning_status(
            digital_test_data, campaign_budget
        )

    @staticmethod
    @pytest.mark.smoke()
    @allure.title("Тест проверки вкладки Аналитика на странице медиаплана. Статус Утвержден")
    @allure.story(jira.JIRA_LINK + 'MDP-5720')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(case.ALLURE_LINK + '401329?treeId=289')
    def test_mplan_analytics_tab_approved_status(
            mediaplan_page: MediaplanPage,
            digital_test_data,
            authorization_in_user_office_with_token,
            office_base_url: str,
    ):
        campaign_data = CampaignsMutationsAPI(authorization_in_user_office_with_token).create_campaign_part_with_budget(
            digital_test_data
        )
        mplan_data = MplansMutationsAPI(authorization_in_user_office_with_token).create_mplan_part(
            campaign_data['data']['campaignCreate']['id']
        )
        placement_data = PlacementMutationsAPI(authorization_in_user_office_with_token).create_placement_part_mts_dsp(
            mplan_data['data']['mplanPlanningCreate']['id'], digital_test_data
        )
        TargetingMutationsAPI(authorization_in_user_office_with_token).add_targeting_descriptions(
            placement_data['data']['placementCreate']['id']
        )
        PlacementMutationsAPI(authorization_in_user_office_with_token).add_placement_metric_budget(
            placement_data['data']['placementCreate']['id']
        )
        PlacementMutationsAPI(authorization_in_user_office_with_token).setup_placement_completed_status(
            placement_data['data']['placementCreate']['id']
        )
        PlacementMutationsAPI(authorization_in_user_office_with_token).approve_placement(
            mplan_data['data']['mplanPlanningCreate']['id'], placement_data['data']['placementCreate']['id']
        )
        campaign_budget = campaign_data['data']['campaignCreate']['budget']
        placement_budget = PlacementQueriesAPI(
            authorization_in_user_office_with_token).get_metrics_and_conversions(
            mplan_data['data']['mplanPlanningCreate']['id'], placement_data['data']['placementCreate']['id']
        )['data']['placementMetrics']['metrics'][0]['value']
        mediaplan_page.visit(DigitalUrl.get_url_digital_mplan_page(
            office_base_url, mplan_data['data']['mplanPlanningCreate']['id']
            )
        )
        mediaplan_page.digital_mediaplan.open_analytics_tab()
        mediaplan_page.digital_mediaplan_analytics.check_analytics_page_approved_status(
            digital_test_data, campaign_budget, placement_budget
        )



