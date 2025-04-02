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
from user_office.components.pages.mediaplan.create_mediaplan_page import (
    CreateMediaplanPage,
)
from user_office.components.pages.mediaplan.mediaplan_page import MediaplanPage
from user_office.components.pages.placement.placement_page import PlacementPage
from user_office.api_interactions.campaign.campaign_api_interactions import CampaignsMutationsAPI
from helper.url_constructor import DigitalUrl


@pytest.mark.usefixtures('authorization_in_user_office_with_token')
class TestMediaPlan:
    @staticmethod
    @pytest.mark.smoke()
    @allure.story(jira.JIRA_LINK + 'MDP-2575')
    @allure.issue('MDP-2504')
    @allure.testcase(case.ALLURE_LINK + '185965?treeId=289')
    @allure.title('Смоук-тест создания Медиаплана. Статус Планирование')
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_mediaplan_planning_status(
            campaign_page: CampaignPage,
            campaigns_list_page: CampaignsListPage,
            create_campaign_page: CreateCampaignPage,
            mediaplan_page: MediaplanPage,
            create_mediaplan_page: CreateMediaplanPage,
            placement_page: PlacementPage,
            digital_test_data,
            authorization_in_user_office_with_token,
            office_base_url: str,
    ) -> None:
        campaign_id = CampaignsMutationsAPI(authorization_in_user_office_with_token).create_campaign_full(
            digital_test_data
        )
        create_mediaplan_page.visit(DigitalUrl.get_url_digital_create_mp_page(office_base_url, campaign_id))
        create_mediaplan_page.digital_create_mediaplan.create_mplan()
        mediaplan_page.digital_mediaplan.check_new_mediaplan_planning_status_through_mp_page(
            digital_test_data['campaign_naming']
        )
        mediaplan_page.digital_mediaplan.open_campaign_page()
        campaign_page.digital_campaign.close_first_mp_notification()
        campaign_page.digital_campaign.check_new_mediaplan_planning_status()

    @staticmethod
    @pytest.mark.regress()
    @allure.story(jira.JIRA_LINK + 'MDP-3452')
    @allure.issue('MDP-3452')
    @allure.testcase(
        case.ALLURE_LINK + '#'
    )  # TODO: требуется доработка/создание тест кейса
    @allure.title('Тест создания черновика Медиаплана')
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_draft_mediaplan(
            campaign_page: CampaignPage,
            campaigns_list_page: CampaignsListPage,
            create_campaign_page: CreateCampaignPage,
            mediaplan_page: MediaplanPage,
            create_mediaplan_page: CreateMediaplanPage,
            placement_page: PlacementPage,
            digital_test_data,
            authorization_in_user_office_with_token,
            office_base_url: str,
    ) -> None:
        campaign_id = CampaignsMutationsAPI(authorization_in_user_office_with_token).create_campaign_full(
            digital_test_data
        )
        create_mediaplan_page.visit(DigitalUrl.get_url_digital_create_mp_page(office_base_url, campaign_id))
        create_mediaplan_page.digital_create_mediaplan.create_draft_mplan()
        mediaplan_page.digital_mediaplan.open_campaign_click_back_btn()
        campaign_page.digital_campaign.close_first_mp_notification()
        create_mediaplan_page.digital_create_mediaplan.check_status_draft_mp()
        campaign_page.digital_campaign.check_mediaplan_draft_status()
