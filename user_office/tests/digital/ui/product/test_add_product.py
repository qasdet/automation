import allure
import pytest

from user_office.components.pages.authorization.authorization_page import (
    AuthorizationPage,
)
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


@pytest.mark.usefixtures('authorization_in_user_office')
class TestCreateMediaPlan:
    @pytest.mark.skip()
    @allure.story('https://jira.mts.ru/browse/MDP-2575')
    @allure.issue('https://jira.mts.ru/browse/MDP-2504')
    @allure.testcase('#185965')
    @allure.description('Смоук тест для создания медиаплана')
    @allure.title('Смоук-тест создание Медиаплана')
    @allure.severity(allure.severity_level.NORMAL)
    @staticmethod
    def test_create_media_plan(
        user_office_authorization: AuthorizationPage,
        campaign_page: CampaignPage,
        campaigns_list_page: CampaignsListPage,
        create_campaign_page: CreateCampaignPage,
        mediaplan_page: MediaplanPage,
        create_mediaplan_page: CreateMediaplanPage,
        placement_page: PlacementPage,
        data_for_campaign,
        data_for_placement,
        data_for_targeting,
        office_base_url: str,
    ) -> None:
        user_office_authorization.visit(url=office_base_url)
        campaigns_list_page.digital_campaigns_list.click_create_campaign_button()
        create_campaign_page.digital_create_campaign.create_campaign_full(
            data_campaign=data_for_campaign
        )
        create_campaign_page.digital_create_campaign.create_campaign_with_two_products(
            data_campaign=data_for_campaign
        )
        campaign_page.digital_campaign.open_create_mediaplan_page()
        create_mediaplan_page.digital_create_mediaplan.create_mplan(
            data_for_targeting
        )
        mediaplan_page.digital_mediaplan.add_placement()
        placement_page.digital_placement_content.create_placement_completed_status_with_budget_metric(
            data_for_placement, data_for_targeting
        )
        mediaplan_page.digital_mediaplan.check_new_placement_completed_status(
            data_for_placement
        )
        # TODO: переделать тест, это полностью скопированый тест на создание медиаплана без проверки создания
