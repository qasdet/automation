import allure
import pytest

from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira
from user_office.components.pages.campaigns.campaign_page import CampaignPage
from user_office.components.pages.campaigns.campaigns_list_page import (
    CampaignsListPage,
)
from user_office.components.pages.campaigns.create_campaign_page import (
    CreateCampaignPage,
)
from user_office.components.pages.mediaplan.create_mediaplan_page import (
    CreateMediaplanPage,
)
from user_office.components.pages.mediaplan.mediaplan_page import MediaplanPage
from user_office.components.pages.placement.placement_page import PlacementPage
from user_office.api_interactions.campaign.campaign_api_interactions import CampaignsMutationsAPI
from user_office.api_interactions.mediaplan.mediaplan_api_interactions import MplansMutationsAPI
from user_office.api_interactions.placement.placement_api_interactions import PlacementMutationsAPI
from user_office.api_interactions.targeting.targeting_api_interactions import TargetingMutationsAPI
from helper.url_constructor import DigitalUrl


@pytest.mark.usefixtures('authorization_in_user_office_with_token')
class TestConnectionSettings:
    @staticmethod
    @pytest.mark.regress()
    @allure.title('Заполнение настроек подключений. Яндекс Директ')
    @allure.story(jira.JIRA_LINK + 'MDP-4334')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(case.ALLURE_LINK + '337463?treeId=289')
    def test_fill_connection_settings_yandex_direct(
            campaign_page: CampaignPage,
            campaigns_list_page: CampaignsListPage,
            create_campaign_page: CreateCampaignPage,
            mediaplan_page: MediaplanPage,
            create_mediaplan_page: CreateMediaplanPage,
            placement_page: PlacementPage,
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
        placement_data = PlacementMutationsAPI(authorization_in_user_office_with_token).create_placement_part_yandex_direct(
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
        create_mediaplan_page.visit(DigitalUrl.get_url_digital_mplan_page(office_base_url,
                                                                          mplan_data['data']['mplanPlanningCreate']
                                                                          ['id']))
        mediaplan_page.digital_mediaplan.open_connection_settings_through_context_menu()
        placement_page.digital_placement.create_connection_yandex_direct()
        mediaplan_page.digital_mediaplan.open_connection_settings_through_context_menu()
        placement_page.digital_placement.check_all_fields_yandex_direct()

    @staticmethod
    @pytest.mark.regress()
    @allure.title('Заполнение настроек подключений. AppsFlyer')
    @allure.story(jira.JIRA_LINK + 'MDP-5027')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(case.ALLURE_LINK + '345147?treeId=289')
    def test_fill_connection_settings_post_click_appsflyer(
            campaign_page: CampaignPage,
            campaigns_list_page: CampaignsListPage,
            create_campaign_page: CreateCampaignPage,
            mediaplan_page: MediaplanPage,
            create_mediaplan_page: CreateMediaplanPage,
            placement_page: PlacementPage,
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
        create_mediaplan_page.visit(DigitalUrl.get_url_digital_mplan_page(office_base_url,
                                                                          mplan_data['data']['mplanPlanningCreate']
                                                                          ['id']))
        mediaplan_page.digital_mediaplan.open_connection_settings_through_context_menu()
        placement_page.digital_placement.create_connection_post_click_appsflyer()
        mediaplan_page.digital_mediaplan.open_connection_settings_through_context_menu()
        placement_page.digital_placement.check_all_fields_post_click_appsflyer()
