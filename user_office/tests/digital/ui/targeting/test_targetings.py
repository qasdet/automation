import allure
import pytest
from helper.url_constructor import DigitalUrl
from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira
from user_office.components.pages.placement.placement_page import PlacementPage
from user_office.api_interactions.campaign.campaign_api_interactions import (
    CampaignsMutationsAPI
)
from user_office.api_interactions.mediaplan.mediaplan_api_interactions import MplansMutationsAPI
from user_office.api_interactions.placement.placement_api_interactions import PlacementMutationsAPI, PlacementQueriesAPI
from user_office.api_interactions.targeting.targeting_api_interactions import TargetingMutationsAPI


@pytest.mark.usefixtures('authorization_in_user_office_with_token')
class TestVerifyTargetingPageInPlacementPageUserOffice:
    """Верификация страницы таргетига в размещении"""

    @staticmethod
    @pytest.mark.smoke()
    @allure.title("Проверяется страница таргетингов в размещении")
    @allure.story(jira.JIRA_LINK + 'MDP-5495')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(case.ALLURE_LINK + '')
    def test_verify_targetings_in_placement(
            placement_page: PlacementPage,
            digital_test_data,
            authorization_in_user_office_with_token,
            office_base_url: str,
    ):
        campaign_id = CampaignsMutationsAPI(authorization_in_user_office_with_token).create_campaign_full(
            digital_test_data
        )
        mplan_data = MplansMutationsAPI(authorization_in_user_office_with_token).create_mplan_full(
            campaign_id, digital_test_data
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
        placement_id = PlacementQueriesAPI(authorization_in_user_office_with_token).get_placement_by_id(
            placement_data['data']['placementCreate']['id']
        )
        placement_page.visit(DigitalUrl.get_url_digital_placement_page(office_base_url, str(
            mplan_data['data']['mplanPlanningCreate']['id']), str(placement_id['data']['placements'][0]['id'])))
        placement_page.digital_placement.create_placement_targetings(digital_test_data)
        placement_page.digital_placement.check_filled_placement_targetings()
