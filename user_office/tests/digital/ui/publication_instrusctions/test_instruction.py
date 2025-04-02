import allure
import pytest

from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira
from helper.url_constructor import DigitalUrl
from user_office.components.pages.campaigns.campaign_page import CampaignPage
from user_office.components.pages.campaigns.campaigns_list_page import (
    CampaignsListPage,
)
from user_office.components.pages.campaigns.create_campaign_page import (
    CreateCampaignPage,
)
from user_office.components.pages.instructions_for_publication.instruction_page import (
    InstructionsPage,
)
from user_office.components.pages.mediaplan.create_mediaplan_page import (
    CreateMediaplanPage,
)
from user_office.components.pages.mediaplan.mediaplan_page import MediaplanPage
from user_office.components.pages.placement.placement_page import PlacementPage
from user_office.api_interactions.campaign.campaign_api_interactions import (
    CampaignsMutationsAPI,
)
from user_office.api_interactions.connections.connections_api_interactions import ConnectionSettingsMutationsAPI
from user_office.api_interactions.mediaplan.mediaplan_api_interactions import MplansMutationsAPI
from user_office.api_interactions.placement.placement_api_interactions import PlacementMutationsAPI
from user_office.api_interactions.targeting.targeting_api_interactions import TargetingMutationsAPI


@pytest.mark.usefixtures('authorization_in_user_office_with_token')
class TestPublicationsInstructions:
    """Форма инструкции по публикации"""

    @staticmethod
    @allure.story(jira.JIRA_LINK + '')
    @allure.testcase(case.ALLURE_LINK + '#185965')
    @allure.description('Владиация страницы настроек публикации')
    @allure.title('Владиация страницы настроек публикации')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_validate_page_instruction_for_publication(
            instruction: InstructionsPage,
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
        campaign_id = CampaignsMutationsAPI(authorization_in_user_office_with_token).create_campaign_part(
            digital_test_data)
        mplan_data = MplansMutationsAPI(authorization_in_user_office_with_token).create_mplan_part(
            campaign_id
        )
        placement_data = PlacementMutationsAPI(
            authorization_in_user_office_with_token).create_placement_part_mts_dsp_add_random_channel(
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
        create_mediaplan_page.visit(DigitalUrl.get_url_digital_campaign_page(office_base_url, campaign_id))
        campaign_page.digital_campaign.open_mediaplan()
        mediaplan_page.digital_mediaplan.open_instructions_publication_from_context_menu()
        instruction.instructions_for_publications.check_all_instructions_page()

    @staticmethod
    @allure.story(jira.JIRA_LINK + 'MDP-5331')
    @allure.testcase(case.ALLURE_LINK + '#')
    @allure.title('Тест публикации размещения')
    @allure.description('Публикация размещения через UI')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_publication_instruction(
            instruction: InstructionsPage,
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
        campaign_id = CampaignsMutationsAPI(authorization_in_user_office_with_token).create_campaign_part(
            digital_test_data)
        mplan_data = MplansMutationsAPI(authorization_in_user_office_with_token).create_mplan_part(
            campaign_id
        )
        placement_data = PlacementMutationsAPI(
            authorization_in_user_office_with_token).create_placement_part_mts_dsp_add_random_channel(
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
        create_mediaplan_page.visit(DigitalUrl.get_url_digital_campaign_page(office_base_url, campaign_id))
        campaign_page.digital_campaign.check_published_campaign_page_ui()
        campaign_page.digital_campaign.check_number_order_no_in_mplan_widget(
            mplan_data['data']['mplanPlanningCreate']['id'])
