import allure
import pytest

from openpyxl.reader.excel import load_workbook
from helper.array_helper import create_dictionary_from_list
from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira
from helper.url_constructor import DigitalUrl
from helper.get_data_from_excel import (
    coordinate_list_generator,
    to_substitute_numbers,
    find_names_by_coordinates,
)
from user_office.constants import (
    SIMPLE_MPLAN_XLS_EXPORT,
    MAIN_TAB,
)
from user_office.components.pages.campaigns.campaign_page import CampaignPage
from user_office.components.pages.campaigns.create_campaign_page import CreateCampaignPage
from user_office.components.pages.campaigns.campaigns_list_page import CampaignsListPage
from user_office.api_interactions.campaign.campaign_api_interactions import CampaignsMutationsAPI
from user_office.components.pages.mediaplan.mediaplan_page import MediaplanPage
from user_office.components.pages.mediaplan.create_mediaplan_page import CreateMediaplanPage
from user_office.api_interactions.mediaplan.mediaplan_api_interactions import MplansMutationsAPI
from user_office.components.pages.placement.placement_page import PlacementPage
from user_office.api_interactions.placement.placement_api_interactions import PlacementMutationsAPI
from user_office.api_interactions.targeting.targeting_api_interactions import TargetingMutationsAPI


list_of_keys = [
    'Хеш размещения',
    'Кликовая ссылка размещения',
]


@pytest.mark.usefixtures('authorization_in_user_office_with_token')
class TestExportMediaPlanPlacementDone:
    """Тест создаёт рекламную кампанию и затем медиаплан, а также размещение. Размещение имеет статус "Заполнено".
    Задача: проверить, что после создания РК и МП работает экспорт xlsx-файла,
    а также, что данные в выгруженном файле соответствуют данным в РК и МП"""

    @staticmethod
    @allure.title(
        "Выгрузка медиаплана в xls формате, с размещением, которое имеет статус 'Заполнено'"
    )
    @allure.story(jira.JIRA_LINK + 'MDP-5977')
    @allure.testcase(case.ALLURE_LINK + '426751?treeId=289')
    @allure.testcase(case.ALLURE_LINK + '426752?treeId=289')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regress
    def test_export_xls_utm_params_tab(
        campaign_page: CampaignPage,
        campaigns_list_page: CampaignsListPage,
        create_campaign_page: CreateCampaignPage,
        mediaplan_page: MediaplanPage,
        create_mediaplan_page: CreateMediaplanPage,
        placement_page: PlacementPage,
        digital_test_data,
        office_base_url: str,
        authorization_in_user_office_with_token,
    ) -> None:
        token = authorization_in_user_office_with_token
        campaign_id = CampaignsMutationsAPI(token).create_campaign_full(digital_test_data)
        mplan_data = MplansMutationsAPI(token).create_mplan_part(campaign_id)
        placement_data = PlacementMutationsAPI(token).create_placement_part_yandex_direct(
            mplan_data['data']['mplanPlanningCreate']['id'], digital_test_data
        )
        TargetingMutationsAPI(token).add_targeting_descriptions(
            placement_data['data']['placementCreate']['id'],
        )
        PlacementMutationsAPI(token).add_placement_metric_budget(
            placement_data['data']['placementCreate']['id']
        )
        PlacementMutationsAPI(token).setup_placement_completed_status(
            placement_data['data']['placementCreate']['id']
        )
        create_mediaplan_page.visit(DigitalUrl.get_url_digital_mplan_page(office_base_url,
                                                                          mplan_data['data']['mplanPlanningCreate']
                                                                          ['id']))
        mediaplan_page.digital_export_mp.export()
        mp_workbook = load_workbook(filename=SIMPLE_MPLAN_XLS_EXPORT)
        main_worksheet = mp_workbook[MAIN_TAB]
        # Поиск адресов ячеек, которые содержат искомые именования. Переменная list_of_keys
        names_coordinates_list = coordinate_list_generator(
            main_worksheet, list_of_keys
        )
        # Создание списка адресов, по которым должны находится значения, соответствующие именам в list_of_keys
        values_coordinates_list = to_substitute_numbers(names_coordinates_list, 3)
        final_dict_from_xls = dict(
            zip(
                find_names_by_coordinates(
                    main_worksheet, names_coordinates_list
                ),
                find_names_by_coordinates(
                    main_worksheet, values_coordinates_list
                ),
            )
        )
        create_mediaplan_page.visit(
            DigitalUrl.get_url_digital_placement_page(office_base_url, mplan_data['data']['mplanPlanningCreate']['id'],
                                                      placement_data['data']['placementCreate']['id']))
        mediaplan_page.digital_placement.click_utm_tab()
        mediaplan_page.digital_placement.page.get_by_role("button", name="Сгенерировать ссылку").click()
        mediaplan_page.digital_placement.page.get_by_role("button", name="Скопировать").click()
        with mediaplan_page.digital_placement.page.expect_console_message() as console_output:
            # Запускает в консоль браузера JS-команду
            mediaplan_page.digital_placement.page.evaluate_handle(
                "setTimeout(() => {navigator.clipboard.readText().then((data) => console.log(data))}, 1000)")
            # Клик в браузере, иначе получится ошибка "Document is not focused"
            mediaplan_page.digital_placement.page.mouse.click(x=600, y=600)
        whole_url_result = console_output.value.text
        get_all_utms = whole_url_result.split('?')[1].split('&')
        mts_hash = create_dictionary_from_list(get_all_utms)['utm_mts']
        final_dict_from_ui = {list_of_keys[0]: mts_hash, list_of_keys[1]: whole_url_result}
        assert final_dict_from_ui == final_dict_from_xls, "Значения из личного кабинета не совпадают со значениями " \
                                                          "в xls-файле"
