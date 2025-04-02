import allure
import pytest
from openpyxl import load_workbook
from helper import date_converter
from helper.get_data_from_excel import (
    find_names_by_coordinates,
    to_substitute_numbers,
    coordinate_list_generator,
    list_separator,
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
from user_office.constants import MAIN_TAB, SIMPLE_MPLAN_XLS_EXPORT
from user_office.api_interactions.campaign.campaign_api_interactions import CampaignsMutationsAPI, CampaignsQueriesAPI
from user_office.api_interactions.mediaplan.mediaplan_api_interactions import MplansMutationsAPI, MplanQueriesAPI
from user_office.api_interactions.placement.placement_api_interactions import PlacementMutationsAPI, PlacementQueriesAPI
from user_office.api_interactions.targeting.targeting_api_interactions import TargetingMutationsAPI
from helper.url_constructor import DigitalUrl

list_of_fields_required_to_check = [
    'Бренд',
    'Продукт',
    'Кампания',
    'Цель',
    'Хеш размещения',
    'Название размещения',
    'Продавец',
    'Площадка',
    'Старт',
    'Завершение',
]


@pytest.mark.usefixtures('authorization_in_user_office_with_token')
class TestExportMediaPlanPlacementInProgress:
    """Тест создаёт рекламную кампанию и затем медиаплан, а также размещение. Размещение имеет статус "В работе".
    Задача: проверить, что после создания РК и МП работает экспорт xlsx-файла,
    а также, что данные в выгруженном файле соответствуют данным в РК и МП"""

    @staticmethod
    @pytest.mark.skip('MDP-5596: Фикс тестов с экспортом xls')
    @allure.title(
        "Выгрузка медиаплана в xls формате, с размещением, которое имеет статус 'В работе'"
    )
    @allure.story('MDP-4461')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regress
    def test_export_mp_with_placement_in_progress(
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
        mplan_data = MplansMutationsAPI(authorization_in_user_office_with_token).create_mplan_part(
            campaign_id
        )
        placement_data = PlacementMutationsAPI(authorization_in_user_office_with_token).create_placement_part_mts_dsp(
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
        create_mediaplan_page.visit(DigitalUrl.get_url_digital_mplan_page(office_base_url,
                                                                          mplan_data['data']['mplanPlanningCreate']
                                                                          ['id']))
        mediaplan_page.digital_mediaplan.open_connection_settings_through_placements_list()
        placement_id = mediaplan_page.digital_export_mp.get_id_from_url(-2)
        placement_page.digital_placement.back_to_mediaplan_page()
        mediaplan_page.digital_export_mp.export()
        mp_workbook = load_workbook(filename=SIMPLE_MPLAN_XLS_EXPORT)
        mediaplan_worksheet = mp_workbook[MAIN_TAB]
        names_coordinates_list = coordinate_list_generator(
            mediaplan_worksheet, list_of_fields_required_to_check
        )
        values_coordinates_list = to_substitute_numbers(
            list_separator(names_coordinates_list), 6
        )
        list_of_values_from_xls = find_names_by_coordinates(mediaplan_worksheet, values_coordinates_list)
        campaigns = CampaignsQueriesAPI(authorization_in_user_office_with_token).get_data_from_ad_campaign(campaign_id)
        mplans = MplanQueriesAPI(authorization_in_user_office_with_token).get_data_from_mplan(campaign_id)
        placements = PlacementQueriesAPI(authorization_in_user_office_with_token).get_data_from_placements(placement_id)
        campaign_name = campaigns['campaigns'][0]['name']
        brand_name = campaigns['campaigns'][0]['brand']['name']
        product_name = campaigns['campaigns'][0]['product']['name']
        start_on = date_converter.date_converter_russian_notation(
            campaigns['campaigns'][0]['startOn']
        )
        finish_on = date_converter.date_converter_russian_notation(
            campaigns['campaigns'][0]['finishOn']
        )
        ad_campaign_goal = mplans['mplans'][0]['goal']['name']
        placement_name = placements['placements'][0]['name']
        placement_hash = placements['placements'][0]['naming']
        placement_site = placements['placements'][0]['site']['name']
        placement_seller = placements['placements'][0]['site']['seller'][
            'name'
        ]
        list_of_values_from_api = [
            campaign_name,
            brand_name,
            product_name,
            start_on,
            finish_on,
            ad_campaign_goal,
            placement_name,
            placement_hash,
            placement_site,
            placement_seller,
        ]
        assert sorted(list_of_values_from_api) == sorted(
            list_of_values_from_xls
        ), (
            'Data from Placement '
            "with 'In progress' status"
            ' form and data from xls'
            ' are not the same'
        )
