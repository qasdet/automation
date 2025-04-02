import re
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
    CampaignsQueriesAPI,
)
from user_office.api_interactions.connections.connections_api_interactions import (
    ConnectionSettingsMutationsAPI,
)
from user_office.api_interactions.mediaplan.mediaplan_api_interactions import (
    MplansMutationsAPI,
    MplanQueriesAPI,
)
from user_office.api_interactions.placement.placement_api_interactions import (
    PlacementQueriesAPI,
    PlacementMutationsAPI,
)
from user_office.api_interactions.targeting.targeting_api_interactions import TargetingMutationsAPI


@pytest.mark.usefixtures("authorization_in_user_office_with_token")
class TestPublicationPlacement:
    @staticmethod
    @allure.story(jira.JIRA_LINK + "MDP-5344")
    @allure.testcase(case.ALLURE_LINK + "#")
    @allure.description("Тест публикации размещения через API")
    @pytest.mark.regress
    @allure.title("Публикация инструкции")
    @allure.severity(allure.severity_level.NORMAL)
    def test_placement_publication(
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
        # Добавил принты для вывода статусов медиплана, размещения, РК в консоль
        campaign_id = CampaignsMutationsAPI(
            authorization_in_user_office_with_token
        ).create_campaign_full(digital_test_data)
        mplan_data = MplansMutationsAPI(
            authorization_in_user_office_with_token
        ).create_mplan_part(campaign_id)

        placement_data = PlacementMutationsAPI(
            authorization_in_user_office_with_token
        ).create_placement_part_mts_dsp(
            mplan_data["data"]["mplanPlanningCreate"]["id"], digital_test_data
        )
        TargetingMutationsAPI(
            authorization_in_user_office_with_token
        ).add_targeting_descriptions(
            placement_data["data"]["placementCreate"]["id"],
        )
        TargetingMutationsAPI(
            authorization_in_user_office_with_token
        ).add_targeting_descriptions(
            placement_data["data"]["placementCreate"]["id"],
        )
        PlacementMutationsAPI(
            authorization_in_user_office_with_token
        ).add_placement_metric_budget(placement_data["data"]["placementCreate"]["id"])
        PlacementMutationsAPI(
            authorization_in_user_office_with_token
        ).setup_placement_completed_status(
            placement_data["data"]["placementCreate"]["id"]
        )
        PlacementMutationsAPI(
            authorization_in_user_office_with_token
        ).approve_placement(
            mplan_data["data"]["mplanPlanningCreate"]["id"],
            placement_data["data"]["placementCreate"]["id"],
        )
        mediaplan_status = MplanQueriesAPI(
            authorization_in_user_office_with_token
        ).get_mplan_status(mplan_id=mplan_data["data"]["mplanPlanningCreate"]["id"])
        match = re.findall(r"Утвержден", str(mediaplan_status), re.I)
        assert match == ["Утвержден"]
        print(f"Медиаплан в статусе: {match}")
        ConnectionSettingsMutationsAPI(
            authorization_in_user_office_with_token
        ).base_setup_placement_connection_settings(
            placement_data["data"]["placementCreate"]["id"]
        )
        PlacementMutationsAPI(
            authorization_in_user_office_with_token
        ).setup_placement_published_status(
            placement_data["data"]["placementCreate"]["id"]
        )
        new_placement_data = PlacementQueriesAPI(
            authorization_in_user_office_with_token
        ).get_placement_by_id(placement_data["data"]["placementCreate"]["id"])
        match = re.findall(r"Опубликовано", str(new_placement_data), re.I)
        assert match == ["Опубликовано"]
        print(f"Размещение в статусе: {match}")
        campaign_data = CampaignsQueriesAPI(
            authorization_in_user_office_with_token
        ).get_campaign_by_id(campaign_id)
        print(campaign_data)
        match = re.findall(r'Опубликована', str(campaign_data), re.I)
        assert match == ['Опубликована']
        print(f'Рекламная кампания в статусе: {match}')

    @staticmethod
    @pytest.mark.skip('MDP-5345: [API] [Regress Digital] Публикация размещения (несколько размещений))')
    @allure.story(jira.JIRA_LINK + 'MDP-5345')
    @allure.testcase(case.ALLURE_LINK + '#')
    @allure.description('Тест публикации 2 размещений через API')
    @allure.title('Публикация двух размещений')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regress
    def test_two_placements_publication(
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
        campaign_id = CampaignsMutationsAPI(
            authorization_in_user_office_with_token
        ).create_campaign_full(digital_test_data)
        mplan_data = MplansMutationsAPI(authorization_in_user_office_with_token).create_mplan_part(
            campaign_id
        )
        """Пока что оставил одно размещение, так как метод апрува не принимает строки и список, 
        думаю как-то это обойти, 
        тест падает с ошибкой - ни одно размещение не выбрано"""

        for i in range(2):
            placement_data = PlacementMutationsAPI(
                authorization_in_user_office_with_token).create_placement_part_mts_dsp(
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
            """Метод получает весь список размещений в медиаплане"""
            placement_list = PlacementQueriesAPI(authorization_in_user_office_with_token).get_all_placement_id_mplan(
                mplan_data['data']['mplanPlanningCreate']['id']
            )
            PlacementMutationsAPI(authorization_in_user_office_with_token).approve_placement(
                mplan_data['data']['mplanPlanningCreate']['id'],
                placement_data['data']['placementCreate']['id']
            )
            ConnectionSettingsMutationsAPI(
                authorization_in_user_office_with_token).base_setup_placement_connection_settings(
                placement_data['data']['placementCreate']['id']
            )
        PlacementMutationsAPI(authorization_in_user_office_with_token).setup_placement_published_status(
            placement_data['data']['placementCreate']['id']
        )
        campaign_status = CampaignsQueriesAPI(authorization_in_user_office_with_token).get_campaign_by_id(
            campaign_id
        )
        match = re.findall(r'Частично опубликована', str(campaign_status), re.I)
        print(match)
        assert match == [campaign_status['data']['campaigns'][0]['status']['name']]
        mediaplan_status = MplanQueriesAPI(authorization_in_user_office_with_token).get_mplan_status(
            mplan_id=mplan_data['data']['mplanPlanningCreate']['id']
        )
        match = re.findall(r'Утвержден', str(mediaplan_status), re.I)
        print(match)
        assert match == ['Утвержден']
