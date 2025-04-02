import allure
import pytest

from helper.linkshort import JiraLink as jira
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
class TestCreatePlacementUserOffice:
    @staticmethod
    @allure.title('Создание размещения')
    @allure.description('Тест создает 20 конверсий')
    @allure.story('заглушка')
    @allure.issue(jira.JIRA_LINK + 'MDP-3749')
    @allure.severity(allure.severity_level.NORMAL)
    #@pytest.mark.smoke()
    def test_create_conversion(
        user_office_authorization: AuthorizationPage,
        campaign_page: CampaignPage,
        campaigns_list_page: CampaignsListPage,
        create_campaign_page: CreateCampaignPage,
        mediaplan_page: MediaplanPage,
        create_mediaplan_page: CreateMediaplanPage,
        placement_page: PlacementPage,
        data_for_campaign,
        data_for_targeting,
        data_for_placement,
        office_base_url: str,
    ):
        user_office_authorization.visit(office_base_url)
        campaigns_list_page.digital_campaigns_list.click_create_campaign_button()
        create_campaign_page.digital_create_campaign.create_campaign_full(
            data_for_campaign
        )
        campaign_page.digital_campaign.open_create_mediaplan_page()
        create_mediaplan_page.digital_create_mediaplan.create_mplan(
            data_for_targeting
        )
        mediaplan_page.digital_mediaplan.add_placement()
        placement_page.create_conversion.create_20_conversion()
        placement_page.create_conversion.save_placement()
