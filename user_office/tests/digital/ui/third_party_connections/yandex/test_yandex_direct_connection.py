import allure
import pytest

from helper.linkshort import JiraLink as jira
from db_stuff.db_interactions.integration_token_table_interaction import (
    get_integration_token_id,
    delete_integration_token_record_by_id,
    get_source_account_by_integration_token,
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


@pytest.mark.usefixtures('authorization_in_user_office_with_token')
class TestYandexDirectConnection:
    @staticmethod
    @pytest.mark.skip('Запускать можно только локально. Иначе, тест упадёт потому что Яндекс не даёт обращаться. '
                      'Видимо как-то определяет, что запрос идёт из пайплайна.')
    @pytest.mark.order(2)
    @pytest.mark.regress
    @allure.title('UI тест подключения размещения к Яндекс.Директ')
    @allure.story(jira.JIRA_LINK + 'MDP-5510')
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_connection_to_yandex_direct(
            create_mediaplan_page: CreateMediaplanPage,
            mediaplan_page: MediaplanPage,
            authorization_in_user_office_with_token,
            digital_test_data,
            office_base_url: str,
            placement_page: PlacementPage,
            yandex_login,
            yandex_password,
    ):
        token = authorization_in_user_office_with_token
        check_integration_token_specific_record_result = get_integration_token_id(yandex_login)
        if check_integration_token_specific_record_result is False:
            pass
        else:
            delete_integration_token_record_by_id(check_integration_token_specific_record_result)
        campaign_id = CampaignsMutationsAPI(token).create_campaign_part(digital_test_data)
        mediaplan_data = MplansMutationsAPI(token).create_mplan_part(campaign_id)
        mediaplan_id = mediaplan_data['data']['mplanPlanningCreate']['id']
        placement_id = PlacementMutationsAPI(token).create_placement_part_yandex_direct(
            mediaplan_id, digital_test_data)['data']['placementCreate']['id']
        TargetingMutationsAPI(token).add_targeting_descriptions(placement_id)
        PlacementMutationsAPI(token).add_placement_metric_budget(placement_id)
        PlacementMutationsAPI(token).setup_placement_completed_status(placement_id)
        PlacementMutationsAPI(token).approve_placement(
            mediaplan_id, placement_id
        )
        mediaplan_page.page.goto(office_base_url + "mediaplan/digital/" + mediaplan_id + "/placement/" +
                                 placement_id + "/connections")
        account_added_value_ui = \
            placement_page.digital_placement.connections.yandex_direct_stat_gathering_method_automatic()
        placement_page.digital_placement.save_button.click()
        assert get_integration_token_id(yandex_login), "Добавленного Яндекс-аккаунта нет в базе"
        account_added_value_db = get_source_account_by_integration_token(
            get_integration_token_id(yandex_login))
        assert account_added_value_db == account_added_value_ui, "Значение из базы и значение из ЛК не совпадают"
        delete_integration_token_record_by_id(get_integration_token_id(yandex_login))
