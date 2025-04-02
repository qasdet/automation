import re
import allure
import pytest

from db_stuff.db_interactions.placement_statuses_db_interactions import (
    get_name_status_by_id_of_placements_status_id_in_the_placement
)
from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira
from user_office.api_interactions.campaign.campaign_api_interactions import (
    CampaignsMutationsAPI,
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


class TestApproveMultiplePlacement:
    @staticmethod
    @allure.story(jira.JIRA_LINK + 'MDP-5979')
    @allure.testcase(case.ALLURE_LINK + '407724?treeId=289')
    @allure.title('Утверждение нескольких размещений единовременно')
    @allure.description('Утверждение нескольких размещений единовременно')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regress
    def test_approve_multiple_placements(
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
        placement_list = PlacementQueriesAPI(authorization_in_user_office_with_token).get_all_placement_id_mplan(
            mplan_data['data']['mplanPlanningCreate']['id']
        )
        approve_list = [
            placement_list["data"]["placements"][0]["id"],
            placement_list["data"]["placements"][1]["id"],
        ]
        PlacementMutationsAPI(authorization_in_user_office_with_token).approve_placement(
            mplan_data['data']['mplanPlanningCreate']['id'],
            approve_list
        )
        mediaplan_status = MplanQueriesAPI(
            authorization_in_user_office_with_token
        ).get_mplan_status(mplan_id=mplan_data["data"]["mplanPlanningCreate"]["id"])
        match = re.findall(r"Утвержден", str(mediaplan_status), re.I)
        assert match == ["Утвержден"]
        print(f'Медиаплан {mplan_data["data"]["mplanPlanningCreate"]["id"]} в статусе: {match}')

        for i in approve_list:
            new_placement_data = PlacementQueriesAPI(authorization_in_user_office_with_token).get_placement_by_id(
                i)
            match = re.findall(r"Уточнение настроек", str(new_placement_data), re.I)
            assert match == ["Уточнение настроек"]
            print(f"Размещение {approve_list[0]} в статусе: {match}")

    @staticmethod
    @allure.story(jira.JIRA_LINK + 'MDP-5974')
    @allure.testcase(case.ALLURE_LINK + '407724?treeId=289')
    @allure.title('Утверждение нескольких размещений единовременно и проверка статуса')
    @allure.description('Утверждение нескольких размещений единовременно и проверка статус в базе данных')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_approve_multiple_placements_check_in_status_from_database(
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
        for i in range(11):
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
        placement_list = PlacementQueriesAPI(authorization_in_user_office_with_token).get_all_placement_id_mplan(
            mplan_data['data']['mplanPlanningCreate']['id']
        )
        approve_list = [
            placement_list["data"]["placements"][0]["id"],
            placement_list["data"]["placements"][1]["id"],
            placement_list["data"]["placements"][2]["id"],
            placement_list["data"]["placements"][3]["id"],
            placement_list["data"]["placements"][4]["id"],
            placement_list["data"]["placements"][5]["id"],
            placement_list["data"]["placements"][6]["id"],
            placement_list["data"]["placements"][7]["id"],
            placement_list["data"]["placements"][8]["id"],
            placement_list["data"]["placements"][9]["id"],
            placement_list["data"]["placements"][10]["id"],
        ]
        PlacementMutationsAPI(authorization_in_user_office_with_token).approve_placement(
            mplan_data['data']['mplanPlanningCreate']['id'],
            approve_list
        )
        mediaplan_status = MplanQueriesAPI(
            authorization_in_user_office_with_token
        ).get_mplan_status(mplan_id=mplan_data["data"]["mplanPlanningCreate"]["id"])
        match = re.findall(r"Утвержден", str(mediaplan_status), re.I)
        assert match == ["Утвержден"]
        print(f'Медиаплан {mplan_data["data"]["mplanPlanningCreate"]["id"]} в статусе: {match}')

        for i in approve_list:
            status = get_name_status_by_id_of_placements_status_id_in_the_placement(i)
            match = re.findall(r"Уточнение настроек", str(status), re.I)
            assert match == ["Уточнение настроек"]
            print(f"Размещение {approve_list} в статусе: {match}")
