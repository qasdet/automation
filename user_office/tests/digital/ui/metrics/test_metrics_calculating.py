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
from user_office.api_interactions.mediaplan.mediaplan_api_interactions import MplansMutationsAPI
from helper.url_constructor import DigitalUrl


@pytest.mark.usefixtures('authorization_in_user_office_with_token')
class TestMetricsCalculating:
    @staticmethod
    @pytest.mark.regress()
    @pytest.mark.skip('MDP-6515')
    @allure.title('Тест расчета метрик. CPM, CPC, CTR')
    @allure.story(jira.JIRA_LINK + 'MDP-4014')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(case.ALLURE_LINK + '185865?treeId=289')
    def test_calculating_metrics_cpm_cpc_ctr(
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
        campaign_id = CampaignsMutationsAPI(authorization_in_user_office_with_token).create_campaign_full(
            digital_test_data
        )
        mplan_data = MplansMutationsAPI(authorization_in_user_office_with_token).create_mplan_part(
            campaign_id
        )
        create_mediaplan_page.visit(DigitalUrl.get_url_digital_mplan_page(
            office_base_url, mplan_data['data']['mplanPlanningCreate']['id']
            )
        )
        mediaplan_page.digital_mediaplan.add_placement()
        placement_page.digital_placement.create_placement_for_metrics_calculating()
        placement_page.digital_placement.check_calculated_metrics_cpm_cpc_ctr()
