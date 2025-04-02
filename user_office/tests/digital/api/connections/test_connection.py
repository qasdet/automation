import allure
import pytest

from db_stuff.db_interactions.integration_token_table_interaction import get_integration_token_id
from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira
from user_office.api_interactions.campaign.campaign_api_interactions import (
    CampaignsMutationsAPI,
    CampaignsQueriesAPI,
)
from user_office.api_interactions.connections.connections_api_interactions import (
    ConnectionSettingsMutationsAPI,
    ConnectionSettingsQueriesAPI
)
from user_office.api_interactions.mediaplan.mediaplan_api_interactions import MplansMutationsAPI
from user_office.api_interactions.placement.placement_api_interactions import PlacementMutationsAPI, PlacementQueriesAPI
from user_office.api_interactions.targeting.targeting_api_interactions import TargetingMutationsAPI


@pytest.mark.usefixtures('authorization_in_user_office_with_token')
class TestReportDigitalConnections:
    @staticmethod
    @pytest.mark.regress()
    @allure.title(
        'API тест создания и проверки виджета подключений, в состоянии настроек - Не заполнено'
    )
    @allure.story(jira.JIRA_LINK + 'MDP-5491')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(case.ALLURE_LINK + '187392?treeId=289')
    def test_report_digital_no_filled_connections_settings(
            digital_test_data,
            authorization_in_user_office_with_token,
            office_base_url: str,
    ):
        campaign_id = CampaignsMutationsAPI(
            authorization_in_user_office_with_token
        ).create_campaign_full(digital_test_data)
        mplan_data = MplansMutationsAPI(
            authorization_in_user_office_with_token
        ).create_mplan_part(campaign_id)
        for i in range(3):
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
            PlacementQueriesAPI(
                authorization_in_user_office_with_token
            ).get_placement_by_id(placement_data["data"]["placementCreate"]["id"])
            CampaignsQueriesAPI(
                authorization_in_user_office_with_token
            ).get_campaign_by_id(campaign_id)
        connections = ConnectionSettingsQueriesAPI(authorization_in_user_office_with_token).get_report_connection_widget(
            mplan_data["data"]["mplanPlanningCreate"]["id"]
        )
        assert connections['data']['reportDigitalConnections']['data'][0]['metrics'][3] == '3', "значение отличается"
        assert connections['data']['reportDigitalConnections']['data'][0]['metrics'][3] == '3', "значение отличается"
        assert connections['data']['reportDigitalConnections']['data'][0]['metrics'][3] == '3', "значение отличается"
        assert connections['data']['reportDigitalConnections']['data'][0]['metrics'][3] == '3', "значение отличается"

    @staticmethod
    @pytest.mark.regress()
    @allure.title(
        'API тест создания и проверки виджета подключений, частичное заполнение'
    )
    @allure.story(jira.JIRA_LINK + 'MDP-6254')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(case.ALLURE_LINK + '193330?treeId=289')
    def test_report_digital_connections_part_filled(
            digital_test_data,
            authorization_in_user_office_with_token,
            office_base_url: str,
            yandex_login: str,
    ):
        campaign_id = CampaignsMutationsAPI(
            authorization_in_user_office_with_token
        ).create_campaign_full(digital_test_data)
        mplan_data = MplansMutationsAPI(
            authorization_in_user_office_with_token
        ).create_mplan_part(campaign_id)
        for i in range(3):
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
            PlacementMutationsAPI(authorization_in_user_office_with_token).approve_placement(
                mplan_data['data']['mplanPlanningCreate']['id'], placement_data['data']['placementCreate']['id']
            )
            match i:
                case 0:
                    print("Первое размещение")
                    ConnectionSettingsMutationsAPI(
                        authorization_in_user_office_with_token).base_setup_placement_connection_settings(
                        placement_data["data"]["placementCreate"]["id"]
                    )
                case 1:
                    print("Второе размещение")
                    integration_token_id = get_integration_token_id(yandex_login)
                    ConnectionSettingsMutationsAPI(
                        authorization_in_user_office_with_token).setup_connection_settings_with_only_one_post_click_tool_auto(
                        placement_data["data"]["placementCreate"]["id"], digital_test_data,
                        integration_token_id
                    )
                case 2:
                    print("Третье размещение")
                    integration_token_id = get_integration_token_id(yandex_login)
                    ConnectionSettingsMutationsAPI(
                        authorization_in_user_office_with_token).setup_connection_settings_with_source_manual_and_post_click_tool_auto(
                        placement_data["data"]["placementCreate"]["id"], digital_test_data,
                        integration_token_id
                    )
        connections = ConnectionSettingsQueriesAPI(authorization_in_user_office_with_token).get_report_connection_widget(
            mplan_data["data"]["mplanPlanningCreate"]["id"]
        )
        assert connections['data']['reportDigitalConnections']['data'][0]['metrics'][1] == '2', "значение отличается"
        assert connections['data']['reportDigitalConnections']['data'][1]['metrics'][2] == '1', "значение отличается"
        assert connections['data']['reportDigitalConnections']['data'][2]['metrics'][3] == '2', "значение отличается"
        assert connections['data']['reportDigitalConnections']['data'][3]['metrics'][2] == '2', "значение отличается"
