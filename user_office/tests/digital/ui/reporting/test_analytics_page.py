import allure
import pytest

from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira
from db_stuff.db_interactions.mplan_conversion_db_interactions import (
    get_metric,
    insert_external_parent_id_in_conversion_ptrs
)
from user_office.components.pages.mediaplan.mediaplan_page import MediaplanPage
from user_office.components.pages.placement.placement_page import PlacementPage
from user_office.api_interactions.campaign.campaign_api_interactions import CampaignsMutationsAPI
from user_office.api_interactions.connections.connections_api_interactions import ConnectionSettingsMutationsAPI
from user_office.api_interactions.mediaplan.mediaplan_api_interactions import MplansMutationsAPI
from user_office.api_interactions.placement.placement_api_interactions import PlacementMutationsAPI, PlacementQueriesAPI
from user_office.api_interactions.targeting.targeting_api_interactions import TargetingMutationsAPI
from user_office.components.pages.reporting.reporting_page import ReportingPage
from db_stuff.db_interactions.integration_token_table_interaction import get_integration_token_id
from helper.url_constructor import DigitalUrl


@pytest.mark.usefixtures('authorization_in_user_office_with_token')
class TestAnalitycsDataPage:

    @staticmethod
    @allure.title("Проверка вкладки Данные на странице Аналитики с Пост-Кликом")
    @allure.story(jira.JIRA_LINK + 'MDP-5322')
    @allure.testcase(case.ALLURE_LINK + '224444?treeId=289')
    @allure.description('Тест вкладки Данные на странице Аналитика автоматический сбор Яндекс метрик')
    @pytest.mark.regress
    @allure.severity(allure.severity_level.NORMAL)
    def test_analytics_data_post_click_auto(
            reporting_page: ReportingPage,
            mediaplan_page: MediaplanPage,
            placement_page: PlacementPage,
            digital_test_data,
            authorization_in_user_office_with_token,
            office_base_url: str,
            yandex_login: str,
    ):
        campaign_id = CampaignsMutationsAPI(authorization_in_user_office_with_token).create_campaign_part(
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
        MplansMutationsAPI(authorization_in_user_office_with_token).create_conversion_in_mplan(
            mplan_data['data']['mplanPlanningCreate']['id'],
            conversion_name='YANDEX_METRIC_IN_POST_CLICK_DONT_DELETE'
        )
        insert_external_parent_id_in_conversion_ptrs()
        PlacementMutationsAPI(
            authorization_in_user_office_with_token).add_placement_metrics_from_db_budget_cpa_cr_conversions(
            placement_data['data']['placementCreate']['id'],
            get_metric(metric_name='YANDEX_METRIC_IN_POST_CLICK_DONT_DELETE')
        )
        PlacementMutationsAPI(authorization_in_user_office_with_token).setup_placement_completed_status(
            placement_data['data']['placementCreate']['id']
        )
        PlacementMutationsAPI(authorization_in_user_office_with_token).approve_placement(
            mplan_data['data']['mplanPlanningCreate']['id'], placement_data['data']['placementCreate']['id']
        )
        integration_token_id = get_integration_token_id(yandex_login)
        ConnectionSettingsMutationsAPI(
            authorization_in_user_office_with_token).add_setup_placement_connection_settings_yandex_metric_auto_post_click(
            placement_data['data']['placementCreate']['id'], digital_test_data,
            integration_token_id
        )
        PlacementMutationsAPI(authorization_in_user_office_with_token).setup_placement_published_status(
            placement_data['data']['placementCreate']['id']
        )
        reporting_page.visit(DigitalUrl.get_url_digital_data_analitycs_page(office_base_url, campaign_id))
        reporting_page.analitycs_page.checking_is_visibility_of_data_on_the_form()

    @staticmethod
    @allure.title("Проверка вкладки Данные на странице Аналитики")
    @allure.story(jira.JIRA_LINK + 'MDP-5322')
    @allure.testcase(case.ALLURE_LINK + '224444?treeId=289')
    @allure.description('Тест вкладки Данные на странице Аналитика - ручное сбор Яндекс метрик')
    @pytest.mark.regress
    @allure.severity(allure.severity_level.NORMAL)
    def test_analytics_data_post_click_manual(
            reporting_page: ReportingPage,
            mediaplan_page: MediaplanPage,
            placement_page: PlacementPage,
            digital_test_data,
            authorization_in_user_office_with_token,
            office_base_url: str,
    ):
        campaign_id = CampaignsMutationsAPI(authorization_in_user_office_with_token).create_campaign_part(
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
        metrics_and_conv_data = PlacementQueriesAPI(
            authorization_in_user_office_with_token).get_metrics_and_conversions(
            mplan_data['data']['mplanPlanningCreate']['id'], placement_data['data']['placementCreate']['id']
        )
        PlacementMutationsAPI(
            authorization_in_user_office_with_token).add_placement_metrics_budget_cpa_cr_conversions(
            placement_data['data']['placementCreate']['id'],
            metrics_and_conv_data['data']['mplans'][0]['conversions'][0]['id']

        )
        PlacementMutationsAPI(authorization_in_user_office_with_token).setup_placement_completed_status(
            placement_data['data']['placementCreate']['id']
        )
        PlacementMutationsAPI(authorization_in_user_office_with_token).approve_placement(
            mplan_data['data']['mplanPlanningCreate']['id'], placement_data['data']['placementCreate']['id']
        )
        ConnectionSettingsMutationsAPI(
            authorization_in_user_office_with_token).add_setup_placement_connection_settings_yandex_metric_post_click(
            placement_data['data']['placementCreate']['id'], digital_test_data
        )
        PlacementMutationsAPI(authorization_in_user_office_with_token).setup_placement_published_status(
            placement_data['data']['placementCreate']['id']
        )
        reporting_page.visit(DigitalUrl.get_url_digital_data_analitycs_page(office_base_url, campaign_id))
        reporting_page.analitycs_page.checking_is_not_visibility_of_data_on_the_form()
