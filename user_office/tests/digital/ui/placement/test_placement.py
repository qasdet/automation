import allure
import pytest
import random

from helper.value_handler import value_handler_decimal_dot
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
from user_office.api_interactions.placement.placement_api_interactions import PlacementMutationsAPI, PlacementQueriesAPI
from user_office.api_interactions.targeting.targeting_api_interactions import TargetingMutationsAPI
from helper.url_constructor import DigitalUrl


@pytest.mark.usefixtures('authorization_in_user_office_with_token')
class TestCreatePlacementUserOffice:
    """Проверка создания размещения с минимальным заполнением, статус В работе"""

    @staticmethod
    @pytest.mark.smoke()
    @allure.title("Создание размещения. Статус 'В работе'")
    @allure.story(jira.JIRA_LINK + 'MDP-2588')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(case.ALLURE_LINK + '130567')
    def test_create_placement_in_work_status(
            mediaplan_page: MediaplanPage,
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
        mediaplan_page.visit(DigitalUrl.get_url_digital_mplan_page(
            office_base_url, mplan_data['data']['mplanPlanningCreate']['id']
            )
        )
        mediaplan_page.digital_mediaplan.add_placement()
        placement_page.digital_placement.create_placement_in_progress_status(
            digital_test_data
        )
        placement_page.digital_placement.back_to_mediaplan_page()
        mediaplan_page.digital_mediaplan.check_new_placement_draft(
            digital_test_data['placement_name']
        )
        # TODO: https://jira.mts.ru/browse/MDP-6520

    @staticmethod
    @pytest.mark.smoke()
    @allure.title("Создание размещения. Статус 'Заполнено', одна метрика")
    @allure.story(jira.JIRA_LINK + 'MDP-2589')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(case.ALLURE_LINK + '189266')
    def test_create_placement_completed_status(
            mediaplan_page: MediaplanPage,
            create_mediaplan_page: CreateMediaplanPage,
            placement_page: PlacementPage,
            digital_test_data,
            authorization_in_user_office_with_token,
            office_base_url: str,
    ):
        metric_data = {
            'metric_name': digital_test_data['budget_metric_name'],
            'metric_value': str(value_handler_decimal_dot(random.randint(10000, 100000)))
        }
        campaign_id = CampaignsMutationsAPI(authorization_in_user_office_with_token).create_campaign_full(
            digital_test_data
        )
        mplan_data = MplansMutationsAPI(authorization_in_user_office_with_token).create_mplan_full(
            campaign_id, digital_test_data
        )
        mediaplan_page.visit(DigitalUrl.get_url_digital_mplan_page(
            office_base_url, mplan_data['data']['mplanPlanningCreate']['id']
            )
        )
        mediaplan_page.digital_mediaplan.add_placement()
        placement_page.digital_placement.create_placement_completed_status(digital_test_data, metric_data)
        placement_page.digital_placement.back_to_mediaplan_page()
        mediaplan_page.digital_mediaplan.check_new_placement_filled_status(digital_test_data['placement_name'])
        # TODO: https://jira.mts.ru/browse/MDP-6520

    @staticmethod
    @pytest.mark.regress()
    @allure.title("Тест повтора размещения")
    @allure.story(jira.JIRA_LINK + 'MDP-4961')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(case.ALLURE_LINK + '338599?treeId=289')
    def test_retry_placement(
            mediaplan_page: MediaplanPage,
            placement_page: PlacementPage,
            digital_test_data,
            authorization_in_user_office_with_token,
            office_base_url: str,
    ):
        metric_data = {
            'metric_num': '0',
            'metric_name': digital_test_data['budget_metric_name'],
            'metric_value': str(value_handler_decimal_dot(random.randint(100, 999))),
        }
        campaign_id = CampaignsMutationsAPI(authorization_in_user_office_with_token).create_campaign_full(
            digital_test_data
        )
        mplan_data = MplansMutationsAPI(authorization_in_user_office_with_token).create_mplan_full(
            campaign_id, digital_test_data
        )
        mediaplan_page.visit(
            DigitalUrl.get_url_digital_mplan_page(
                office_base_url, mplan_data['data']['mplanPlanningCreate']['id']
            )
        )
        mediaplan_page.digital_mediaplan.add_placement()
        placement_page.digital_placement.create_placement_completed_status(
            digital_test_data, metric_data
        )
        placement_page.digital_placement.back_to_mediaplan_page()
        mediaplan_page.digital_mediaplan.retry_placement()
        placement_page.digital_placement.accept_placement_data_to_retry(
            digital_test_data=digital_test_data, metric_data=metric_data
        )
        placement_page.digital_placement.back_to_mediaplan_page()
        mediaplan_page.digital_mediaplan.open_placement_by_name(
            f'2_{digital_test_data["site_mts_dsp_name"].replace(" ", "")}_{digital_test_data["channel_display_name"]}_'
            f'{digital_test_data["buy_type_cpm_name"]}'
        )
        placement_page.digital_placement.check_retried_placement_data(
            digital_test_data=digital_test_data, metric_data=metric_data
        )


    @staticmethod
    @allure.story(jira.JIRA_LINK + "MDP-5973")
    @allure.testcase(case.ALLURE_LINK + "407020?treeId=289")
    @allure.description("Тест утверждения одного размещения")
    @pytest.mark.smoke
    @allure.title("Утверждение одного размещения")
    @allure.severity(allure.severity_level.NORMAL)
    def test_approve_one_placement_in_mediaplan(
            mediaplan_page: MediaplanPage,
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
        ).create_mplan_full(campaign_id, digital_test_data)

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
        mediaplan_page.visit(
            DigitalUrl.get_url_digital_mplan_page(office_base_url, mplan_data["data"]["mplanPlanningCreate"]["id"]))
        mediaplan_page.digital_mediaplan.checkbox_check()

    @staticmethod
    @allure.story(jira.JIRA_LINK + 'MDP-5736')
    @allure.testcase(case.ALLURE_LINK + '290109?treeId=289')
    @allure.title('Тест добавления размещения в справочник и создания размещения из него')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regress
    def test_create_placement_from_template(
            mediaplan_page: MediaplanPage,
            placement_page: PlacementPage,
            digital_test_data,
            authorization_in_user_office_with_token,
            office_base_url: str,
            delete_placement_template_by_id_in_organization
    ):
        campaign_id = CampaignsMutationsAPI(authorization_in_user_office_with_token).create_campaign_part(
            digital_test_data)
        mplan_data = MplansMutationsAPI(authorization_in_user_office_with_token).create_mplan_part(
            campaign_id
        )
        placement_data = PlacementMutationsAPI(
            authorization_in_user_office_with_token).create_placement_part_mts_dsp(
            mplan_data['data']['mplanPlanningCreate']['id'], digital_test_data
        )
        TargetingMutationsAPI(authorization_in_user_office_with_token).add_targeting_descriptions(
            placement_data['data']['placementCreate']['id'],
        )
        PlacementMutationsAPI(
            authorization_in_user_office_with_token
        ).add_placement_benchmark_metrics_for_placement_template(
            placement_data['data']['placementCreate']['id']
        )
        PlacementMutationsAPI(authorization_in_user_office_with_token).setup_placement_completed_status(
            placement_data['data']['placementCreate']['id']
        )
        PlacementMutationsAPI(authorization_in_user_office_with_token).approve_placement(
            mplan_data['data']['mplanPlanningCreate']['id'], placement_data['data']['placementCreate']['id']
        )
        mediaplan_page.visit(DigitalUrl.get_url_digital_mplan_page(
            office_base_url, mplan_data['data']['mplanPlanningCreate']['id']
        )
        )
        metrics_data = PlacementQueriesAPI(
            authorization_in_user_office_with_token).get_metrics_and_conversions(
            mplan_data['data']['mplanPlanningCreate']['id'], placement_data['data']['placementCreate']['id']
        )
        mediaplan_page.digital_mediaplan.add_placement_to_templates()
        mediaplan_page.digital_mediaplan.add_placement_from_templates_without_conversions(digital_test_data)
        placement_page.digital_placement.check_placement_from_templates_dictionary(
            digital_test_data, metrics_data
        )
