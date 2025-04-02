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
from user_office.api_interactions.mediaplan.mediaplan_api_interactions import (
    MplansMutationsAPI,
)
from user_office.api_interactions.placement.placement_api_interactions import (
    PlacementMutationsAPI, PlacementQueriesAPI,
)
from user_office.api_interactions.targeting.targeting_api_interactions import TargetingMutationsAPI
from db_stuff.db_interactions.placements_db_interactions import (
    delete_placements_record,
)


def read_mplan_id():
    with open("placement.txt", "r", encoding="utf8") as f:
        return f.read()


@pytest.fixture()
def resource():
    print("\nsetup")
    yield "Считался uuid медиаплан"
    """При неудачном и удачном завершении теста сработает очистка всех созданных размещений"""
    uiid_ = read_mplan_id()
    delete_placements_record(uiid_)


@pytest.mark.usefixtures("authorization_in_user_office_with_token")
class TestCreate150PlacementInApi:
    @staticmethod
    @pytest.mark.skip('MDP-6002 доработать и выделить отдельную джобу')
    @allure.story(jira.JIRA_LINK + "MDP-4382")
    @allure.testcase(case.ALLURE_LINK + "#")
    @allure.description(
        "Создание 150 размещений в статусе заполнено с разными каналами"
    )
    @allure.title("Создание 150 размещений через API")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.skip(reason="https://jira.mts.ru/browse/MDP-6002")
    @pytest.mark.regress
    def test_create_150_placement_in_api(
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
            resource,
    ):
        campaign_id = CampaignsMutationsAPI(
            authorization_in_user_office_with_token
        ).create_campaign_part(digital_test_data)

        mplan_data = MplansMutationsAPI(
            authorization_in_user_office_with_token
        ).create_mplan_part(campaign_id)
        with open("placement.txt", "w", encoding="utf8") as f:
            info = mplan_data["data"]["mplanPlanningCreate"]["id"]
            f.writelines(info)
        num = 150
        for i in range(num):
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
        create_mediaplan_page.visit(
            DigitalUrl.get_url_digital_mplan_page(
                office_base_url,
                mplan_data["data"]["mplanPlanningCreate"]["id"],
            )
        )
        mediaplan_page.digital_mediaplan.pagination_in_page_mediaplan_1_level()
        mediaplan_page.digital_mediaplan.pagination_in_page_mediaplan_2_level()
        count = PlacementQueriesAPI(authorization_in_user_office_with_token).get_all_placement_id_mplan(
            mplan_data["data"]["mplanPlanningCreate"]["id"])
        assert count == 150, "Количество размещений меньше 150"
