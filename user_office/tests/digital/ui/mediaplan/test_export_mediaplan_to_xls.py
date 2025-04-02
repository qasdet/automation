import allure
import pytest

from openpyxl.reader.excel import load_workbook
from helper import date_converter
from helper.get_data_from_excel import (
    coordinate_list_generator,
    to_substitute_letters,
    find_names_by_coordinates,
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
from user_office.constants import MAIN_TAB, SIMPLE_MPLAN_XLS_EXPORT
from user_office.api_interactions.campaign.campaign_api_interactions import (
    CampaignsMutationsAPI,
    CampaignsQueriesAPI,
)

list_of_keys = [
    'Клиент',
    'Кампания',
    'Даты кампании'
]


@pytest.mark.usefixtures('authorization_in_user_office_with_token')
class TestExportMediaPlan:
    """Тест создаёт рекламную кампанию.
    Задача: проверить, что после создания РК работает экспорт шаблона xlsx-файла,
    а также, что данные в выгруженном файле соответствуют данным в РК"""

    @staticmethod
    @allure.title('Выгрузка медиаплана в xls формате')
    @allure.description('Тест утверждения МП')
    @allure.story('MDP-3451')
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.smoke
    def test_export_media_plan(
            campaign_page: CampaignPage,
            campaigns_list_page: CampaignsListPage,
            create_campaign_page: CreateCampaignPage,
            mediaplan_page: MediaplanPage,
            create_mediaplan_page: CreateMediaplanPage,
            digital_test_data,
            authorization_in_user_office_with_token,
            office_base_url: str,
    ) -> None:
        token = authorization_in_user_office_with_token
        campaign_id = CampaignsMutationsAPI(token).create_campaign_full(
            digital_test_data
        )
        # Получение информации по созданной РК
        ad_campaign_info_response = CampaignsQueriesAPI(token).get_data_from_ad_campaign(campaign_id)

        # Извлечение имени клиента из вложенного словаря
        ad_campaign_info_response['campaigns'][0]['client'] = ad_campaign_info_response[
            'campaigns'][0]['client']['name']

        # Изменение формата даты с 'YYYY-MM-DDThh:mm:ssZ' на 'DD.MM.YYYY'
        ad_campaign_info_response['campaigns'][0]['startOn'] = date_converter.date_converter_russian_notation(
            ad_campaign_info_response['campaigns'][0]['startOn'])
        ad_campaign_info_response['campaigns'][0]['finishOn'] = date_converter.date_converter_russian_notation(
            ad_campaign_info_response['campaigns'][0]['finishOn'])

        campaign_page.page.goto(office_base_url + "campaigns/digital/" + campaign_id)
        campaign_page.digital_campaign.click_download_xls_template_link()

        # Работа с выгруженным xslx-файлом. Ищет вкладку, переходит на неё.
        mp_workbook = load_workbook(filename=SIMPLE_MPLAN_XLS_EXPORT)
        # mp_worksheet = mp_workbook.active
        main_worksheet = mp_workbook[MAIN_TAB]
        # Поиск адресов ячеек, которые содержат искомые именования. Переменная list_of_keys
        names_coordinates_list = coordinate_list_generator(
            main_worksheet, list_of_keys
        )
        # Создание списка адресов, по которым должны находится значения, соответствующие именам в list_of_keys
        values_coordinates_list = to_substitute_letters(
            list_separator(names_coordinates_list)
        )
        # Формирование словаря, где ключом выступают имена из list_of_keys, а значениями, то что мы нашли по адресам.
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

        data_from_server = {'Клиент': ad_campaign_info_response['campaigns'][0]['client'],
                            'Кампания': ad_campaign_info_response['campaigns'][0]['name'],
                            'Даты кампании': ad_campaign_info_response['campaigns'][0]['startOn'] +
                            ' - ' + ad_campaign_info_response['campaigns'][0]['finishOn']
                            }
        assert data_from_server == final_dict_from_xls, 'Значения в словарях должны быть идентичны'
