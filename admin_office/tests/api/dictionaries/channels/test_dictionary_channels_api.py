import allure
import pytest
import humps

from helper.array_helper import compare_the_response_from_service_with_expected_response
from admin_office.api_interactions.channels.channels_api_interactions import (
    create_channel_api,
    edit_channel_api,
    get_specific_channel_by_code_api,
    get_channels_api,
)
from helper.array_helper import compare_lists_of_dictionaries
from admin_office.components.pages.channels.channels_page import AdminOfficeChannelsPage
from admin_office.tests.api.dictionaries.channels.data_generator_for_channel import get_data_for_channel
from db_stuff.db_interactions.channels_db_interactions import (
    get_list_of_channels_from_db,
    get_channel_by_code,
    delete_channel_by_code)
from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira

data_channel = get_data_for_channel()


@pytest.mark.usefixtures('authorization_in_admin_office_with_token')
class TestsDictionaryChannelsAPI:
    @staticmethod
    @pytest.mark.order(1)
    @pytest.mark.regress()
    @allure.title('Создание канала через API')
    @allure.story(jira.JIRA_LINK + 'MDP-416')
    @allure.testcase(case.ALLURE_LINK + '122452')
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_channel_api(
            admin_channels_page: AdminOfficeChannelsPage,
            authorization_in_admin_office_with_token: str,
    ) -> None:
        """Создание канала"""
        token = authorization_in_admin_office_with_token
        result_of_creation = create_channel_api(data_channel['name'],
                                                data_channel['code'],
                                                data_channel['naming'],
                                                data_channel['media_type'],
                                                data_channel['is_used_by_splan'],
                                                token,
                                                )
        check_created_channel = get_specific_channel_by_code_api(data_channel['code'], token)['data']['adminChannels'][
            0]
        check_channel_in_db = get_channel_by_code(data_channel['code'])
        channel_data_taken_from_db = {'name': check_channel_in_db.name,
                                      'naming': check_channel_in_db.naming,
                                      'code': check_channel_in_db.code,
                                      'mediaType': check_channel_in_db.media_type,
                                      'isUsedBySplan': check_channel_in_db.is_used_by_splan}
        result_of_creation = result_of_creation['data']['adminChannelCreate']
        assert result_of_creation == check_created_channel, "Данные полученные после создания и данные полученные с" \
                                                            " сервера не совпадают"
        assert result_of_creation == channel_data_taken_from_db, "Данные полученные после создания и данные из базы" \
                                                                 "не совпадают"

    @staticmethod
    @pytest.mark.order(2)
    @pytest.mark.regress()
    @allure.title('Редактирование канала через API')
    @allure.story(jira.JIRA_LINK + 'MDP-416')
    @allure.testcase(case.ALLURE_LINK + '122452')
    @allure.severity(allure.severity_level.NORMAL)
    def test_edit_channel_api(
            admin_channels_page: AdminOfficeChannelsPage,
            authorization_in_admin_office_with_token: str,
    ):
        token = authorization_in_admin_office_with_token
        """Редактирование канала"""
        data_channel['name'] = data_channel['name'] + '1'
        data_channel['naming'] = data_channel['naming'] + '2'
        response = edit_channel_api(
            data_channel['code'],
            data_channel['name'],
            data_channel['naming'],
            data_channel['media_type'],
            data_channel['is_used_by_splan'],
            token,
        )
        response['media_type'] = response.pop('mediaType')
        response['is_used_by_splan'] = response.pop('isUsedBySplan')
        compare_the_response_from_service_with_expected_response(
            response, data_channel
        )
        delete_channel_by_code((data_channel['code']))

    @staticmethod
    @pytest.mark.order(3)
    @pytest.mark.regress()
    @allure.title('Сравнение списка каналов, полученных через API и выгруженных из БД')
    @allure.story(jira.JIRA_LINK + 'MDP-416')
    @allure.testcase(case.ALLURE_LINK + '122453')
    @allure.severity(allure.severity_level.NORMAL)
    def test_compare_lists_of_channels_from_api_and_db(
            authorization_in_admin_office_with_token,
    ):
        """Получение всех каналов"""
        token = authorization_in_admin_office_with_token
        list_of_channels_from_api = humps.decamelize(get_channels_api(token))
        list_of_channels_from_db = get_list_of_channels_from_db()
        assert len(list_of_channels_from_api) == len(
            list_of_channels_from_db
        ), (
            f'Количество записей от сервиса не равно ожидаемому. '
            f'Фактическое: {len(list_of_channels_from_api)}. Ожидаемое: {len(list_of_channels_from_db)}'
        )
        assert compare_lists_of_dictionaries(
            list_of_channels_from_api,
            list_of_channels_from_db), 'Ответ от сервиса не равен ожидаемому.'
