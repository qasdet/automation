import allure
import pytest

from helper.url_constructor import DigitalUrl
from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira
from user_office.api_interactions.campaign.campaign_api_interactions import (
    CampaignsMutationsAPI, CampaignsQueriesAPI
)
from user_office.api_interactions.mediaplan.mediaplan_api_interactions import MplanQueriesAPI
from user_office.api_interactions.placement.placement_api_interactions import PlacementQueriesAPI
from user_office.components.pages.authorization.authorization_page import (
    AuthorizationPage,
)
from user_office.components.pages.campaigns.campaign_page import CampaignPage
from user_office.components.pages.health_check.health_check_page import (
    HealthCheckPage,
)
from user_office.components.pages.mediaplan.mediaplan_page import MediaplanPage
from user_office.components.pages.placement.placement_page import PlacementPage


@pytest.mark.usefixtures('authorization_in_user_office_with_token')
class TestImportExcelFromTemplate:
    @staticmethod
    @pytest.mark.regress()
    @allure.title(test_title='Импорт шаблона эксель')
    @allure.description(test_description='Создание одного МП из эксель шаблона')
    @allure.severity(severity_level=allure.severity_level.CRITICAL)
    @allure.issue(jira.JIRA_LINK + 'MDP-6335')
    @allure.testcase(case.ALLURE_LINK + '404633')
    def test_create_one_mediaplan_from_import_excel_template(
            user_office_authorization: AuthorizationPage,
            campaign_page: CampaignPage,
            mediaplan_page: MediaplanPage,
            placement_page: PlacementPage,
            authorization_in_user_office_with_token,
            digital_test_data,
            office_base_url: str,
    ) -> None:
        campaign_id = CampaignsMutationsAPI(
            authorization_in_user_office_with_token
        ).create_campaign_full(digital_test_data)
        campaign_name = CampaignsQueriesAPI(authorization_in_user_office_with_token).get_campaign_by_id(campaign_id)
        mediaplan_page.visit(DigitalUrl.get_url_digital_campaign_page(office_base_url, campaign_id))
        mediaplan_page.import_excel.fill_excel_files(campaign_name['data']['campaigns'][0]['name'],
                                                     campaign_name['data']['campaigns'][0]['client']['name'])
        mediaplan_page.import_excel.upload_media_plan()
        mediaplan_page.import_excel.check_upload_excel_template()
        mediaplan_page.visit(DigitalUrl.get_url_digital_campaign_page(office_base_url, campaign_id))
        get_mplan_id = MplanQueriesAPI(authorization_in_user_office_with_token).get_mplan_id_query(campaign_id)
        mediaplan_page.visit(DigitalUrl.get_url_digital_mplan_page(office_base_url, mplan_id=get_mplan_id))
        mp_plan_excel = mediaplan_page.import_excel.collect_cell()
        mediaplan_page.digital_mediaplan.check_in_filled_from_import_excel(mp_plan_excel)
        placement_id = PlacementQueriesAPI(authorization_in_user_office_with_token).get_all_placement_id_mplan(
            get_mplan_id
        )
        placement_page.visit(DigitalUrl.get_url_digital_placement_page(office_base_url, get_mplan_id,
                                                                       placement_id['data']['placements'][0]['id']))
        cell = mediaplan_page.import_excel.collect_cell()
        placement_page.digital_placement.composition.check_filled_placement_form_in_excel_file(cell)
        placement_page.digital_placement.clicking_in_tab_targeting()
        placement_page.digital_placement.targeting.check_filled_targeting_textarea_in_excel_file(cell)
        campaign_page.visit(DigitalUrl.get_url_digital_campaign_page(office_base_url, campaign_id))

    @staticmethod
    @pytest.mark.smoke()
    @allure.title(test_title='Импорт шаблона эксель')
    @allure.description(test_description='Создание двух МП из эксель шаблона')
    @allure.severity(severity_level=allure.severity_level.CRITICAL)
    @allure.issue(jira.JIRA_LINK + 'MDP-6336')
    @allure.testcase(case.ALLURE_LINK + '415385?treeId=288')
    def test_create_two_mediaplan_from_import_excel_template(
            user_office_authorization: AuthorizationPage,
            campaign_page: CampaignPage,
            mediaplan_page: MediaplanPage,
            placement_page: PlacementPage,
            authorization_in_user_office_with_token,
            digital_test_data,
            office_base_url: str,
    ) -> None:
        campaign_id = CampaignsMutationsAPI(
            authorization_in_user_office_with_token
        ).create_campaign_full(digital_test_data)
        campaign_name = CampaignsQueriesAPI(authorization_in_user_office_with_token).get_campaign_by_id(campaign_id)
        mediaplan_page.visit(DigitalUrl.get_url_digital_campaign_page(office_base_url, campaign_id))
        mediaplan_page.import_excel.fill_excel_files(campaign_name['data']['campaigns'][0]['name'],
                                                     campaign_name['data']['campaigns'][0]['client']['name'])
        for i in range(2):
            mediaplan_page.import_excel.upload_media_plan()
            mediaplan_page.import_excel.check_upload_excel_template()
        mediaplan_page.visit(DigitalUrl.get_url_digital_campaign_page(office_base_url, campaign_id))

        for i in range(2):
            get_mplan_id = MplanQueriesAPI(authorization_in_user_office_with_token).get_all_mplans_in_campaign(
                campaign_id)
            mediaplan_page.visit(DigitalUrl.get_url_digital_mplan_page(office_base_url,
                                                                       mplan_id=get_mplan_id['data']['mplans'][i][
                                                                           'id']))
            mp_plan_excel = mediaplan_page.import_excel.collect_cell()
            mediaplan_page.digital_mediaplan.check_in_filled_from_import_excel(mp_plan_excel)
            placement_id = PlacementQueriesAPI(authorization_in_user_office_with_token).get_all_placement_id_mplan(
                get_mplan_id['data']['mplans'][i]['id']
            )
            placement_page.visit(
                DigitalUrl.get_url_digital_placement_page(office_base_url, get_mplan_id['data']['mplans'][i]['id'],
                                                          placement_id['data']['placements'][0]['id']))
            cell = mediaplan_page.import_excel.collect_cell()
            placement_page.digital_placement.composition.check_filled_placement_form_in_excel_file(cell)
            placement_page.digital_placement.composition.check_filled_placement_form_in_excel_file(cell)
            placement_page.digital_placement.clicking_in_tab_targeting()
            placement_page.digital_placement.targeting.check_filled_targeting_textarea_in_excel_file(cell)
            campaign_page.visit(DigitalUrl.get_url_digital_campaign_page(office_base_url, campaign_id))
