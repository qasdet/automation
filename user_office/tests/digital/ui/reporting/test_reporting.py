import allure
import pytest

from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira
from user_office.api_interactions.campaign.campaign_api_interactions import CampaignsMutationsAPI
from user_office.api_interactions.connections.connections_api_interactions import ConnectionSettingsMutationsAPI
from user_office.api_interactions.mediaplan.mediaplan_api_interactions import MplansMutationsAPI
from user_office.api_interactions.placement.placement_api_interactions import PlacementMutationsAPI
from user_office.components.pages.reporting.reporting_page import ReportingPage
from user_office.api_interactions.targeting.targeting_api_interactions import TargetingMutationsAPI
from helper.default_dates import get_default_campaign_begin_date_for_ui, get_default_campaign_end_date_for_ui
from helper.url_constructor import DigitalUrl


@pytest.mark.usefixtures('authorization_in_user_office_with_token')
class TestPublicationPlacement:

    @staticmethod
    @allure.story(jira.JIRA_LINK + 'MDP-5320')
    @allure.testcase(case.ALLURE_LINK + '206997?treeId=289')
    @allure.title('Тест страницы План-факт')
    @allure.description(
        'Тест страницы отчета План-факт'
    )
    @pytest.mark.smoke
    @allure.severity(allure.severity_level.NORMAL)
    def test_reporting_page(
            reporting_page: ReportingPage,
            digital_test_data,
            authorization_in_user_office_with_token,
            office_base_url: str,
    ):
        campaign_id = CampaignsMutationsAPI(authorization_in_user_office_with_token).create_campaign_full(
            digital_test_data
        )
        mplan_data = MplansMutationsAPI(authorization_in_user_office_with_token).create_mplan_part(
            campaign_id
        )
        placement_data = PlacementMutationsAPI(authorization_in_user_office_with_token).create_placement_part_mts_dsp(
            mplan_data['data']['mplanPlanningCreate']['id'], digital_test_data
        )
        TargetingMutationsAPI(authorization_in_user_office_with_token).add_targeting_descriptions(
            placement_data['data']['placementCreate']['id'],
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
        ConnectionSettingsMutationsAPI(
            authorization_in_user_office_with_token).base_setup_placement_connection_settings(
            placement_data['data']['placementCreate']['id']
        )
        PlacementMutationsAPI(authorization_in_user_office_with_token).setup_placement_published_status(
            placement_data['data']['placementCreate']['id']
        )
        reporting_page.visit(DigitalUrl.get_url_digital_reporting_page(office_base_url, campaign_id,
                                                                       get_default_campaign_begin_date_for_ui(),
                                                                       get_default_campaign_end_date_for_ui()))
        reporting_page.reporting.check_reporting_page()


