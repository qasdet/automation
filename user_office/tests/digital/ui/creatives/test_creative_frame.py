import allure
import pytest

from helper.linkshort import JiraLink as jira
from helper.linkshort import AllureLink as case
from user_office.components.pages.mediaplan.create_mediaplan_page import (
    CreateMediaplanPage,
)
from user_office.components.pages.mediaplan.mediaplan_page import MediaplanPage
from user_office.components.pages.placement.placement_page import PlacementPage
from user_office.api_interactions.campaign.campaign_api_interactions import CampaignsMutationsAPI
from user_office.api_interactions.mediaplan.mediaplan_api_interactions import MplansMutationsAPI
from user_office.api_interactions.placement.placement_api_interactions import PlacementMutationsAPI
from user_office.api_interactions.targeting.targeting_api_interactions import TargetingMutationsAPI
from helper.names_generator.creative_frame_names_generator import (
    creative_frame_name_generator,
    creative_frame_naming_generator,
)

creative_frame_name = creative_frame_name_generator()
creative_frame_naming = creative_frame_naming_generator(creative_frame_name)
creative_frame_dictionary = {
    'name': creative_frame_name,
    'naming': creative_frame_naming,
}


@pytest.mark.usefixtures('authorization_in_user_office_with_token')
class TestCreativeFrames:
    @staticmethod
    @pytest.mark.smoke
    @allure.title('Создание рамки креатива в размещении')
    @allure.story(jira.JIRA_LINK + 'MDP-5981')
    @allure.testcase(case.ALLURE_LINK + '346352')
    @allure.severity(allure.severity_level.NORMAL)
    def test_creative_frame(
            create_mediaplan_page: CreateMediaplanPage,
            mediaplan_page: MediaplanPage,
            authorization_in_user_office_with_token,
            digital_test_data,
            office_base_url: str,
            placement_page: PlacementPage,

    ):
        token = authorization_in_user_office_with_token
        campaign_id = CampaignsMutationsAPI(token).create_campaign_part(digital_test_data)
        mediaplan_data = MplansMutationsAPI(token).create_mplan_part(campaign_id)
        mediaplan_id = mediaplan_data['data']['mplanPlanningCreate']['id']
        placement_id = PlacementMutationsAPI(token).create_placement_part_yandex_direct(
            mediaplan_id, digital_test_data)['data']['placementCreate']['id']
        TargetingMutationsAPI(authorization_in_user_office_with_token).add_targeting_descriptions(placement_id)
        PlacementMutationsAPI(token).add_placement_metric_budget(placement_id)
        PlacementMutationsAPI(token).setup_placement_completed_status(placement_id)
        PlacementMutationsAPI(token).approve_placement(
            mediaplan_id, placement_id
        )
        mediaplan_page.page.goto(office_base_url + "mediaplan/digital/" + mediaplan_id + "/placement/" +
                                 placement_id + "/creatives")
        placement_page.digital_placement.creatives.click_add_creative_button()
        placement_page.digital_placement.creatives.click_create_creative_frame_button()
        placement_page.digital_placement.creatives.fill_creative_frame_name_field(creative_frame_name)
        placement_page.digital_placement.creatives.fill_creative_frame_naming_field(creative_frame_naming)
        placement_page.digital_placement.creatives.click_creative_frame_form_submit()
        creative_frame_name_from_ui = placement_page.digital_placement.creatives.page.get_by_test_id(
            'creatives_creative_frame').inner_text()
        assert creative_frame_name == creative_frame_name_from_ui, "Сгенерированное название рамки " \
                                                                   "не совпадает с тем, что отображается в браузере"
