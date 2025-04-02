import allure
import pytest

from admin_office.components.pages.channels.channels_page import AdminOfficeChannelsPage
from admin_office.tests.api.dictionaries.channels.data_generator_for_channel import get_data_for_channel
from db_stuff.db_interactions.channels_db_interactions import delete_channel_by_code
from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira

data_channel = get_data_for_channel()


@pytest.mark.usefixtures('authorization_in_admin_office_with_token')
class TestsDictionaryChannels:
    @staticmethod
    @pytest.mark.order(1)
    @pytest.mark.regress()
    @allure.title('Создание записи в Справочнике Каналы')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story(jira.JIRA_LINK + 'MDP-416')
    @allure.testcase(case.ALLURE_LINK + '121908')
    def test_create_channel(
            admin_channels_page: AdminOfficeChannelsPage,
            authorization_in_admin_office_with_token: str,
    ) -> None:
        """Создание записи в Справочнике Каналы"""
        admin_channels_page.go_to_channels()
        admin_channels_page.channels.open_the_channel_creation_form()
        admin_channels_page.channel_card.fill_all_fields(**data_channel)
        admin_channels_page.channel_card.click_create_channel_button()
        admin_channels_page.channels.check_new_channel(data_channel)

    @staticmethod
    @pytest.mark.order(2)
    @pytest.mark.regress()
    @allure.title(
        'Редактирование записи в Справочнике Каналы через контекстное меню'
    )
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story(jira.JIRA_LINK + 'MDP-416')
    @allure.testcase(case.ALLURE_LINK + '121918')
    def test_edit_channel_through_context_menu(
            admin_channels_page: AdminOfficeChannelsPage,
            authorization_in_admin_office_with_token: str,
    ) -> None:
        """Редактирование записи в Справочнике Каналы через контекстное меню"""
        admin_channels_page.channels.open_the_channel_for_editing_through_context_menu(
            text_row=data_channel['code']
        )
        data_channel['name'] = data_channel['name'] + '1'
        data_channel['naming'] = data_channel['naming'] + '2'
        admin_channels_page.channel_card.fill_required_fields(
            data_channel['name'],
            data_channel['naming'],
        )
        admin_channels_page.channel_card.click_save_channel_button()
        admin_channels_page.page.reload()
        admin_channels_page.channels.check_new_channel(data_channel)

    @staticmethod
    @pytest.mark.order(3)
    @pytest.mark.regress()
    @allure.title('Редактирование записи в Справочнике Каналы')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story(jira.JIRA_LINK + 'MDP-416')
    @allure.testcase(case.ALLURE_LINK + '122144')
    def test_edit_channel(
            admin_channels_page: AdminOfficeChannelsPage,
            authorization_in_admin_office_with_token: str,
    ) -> None:
        """Редактирование записи через контекстное меню в Справочнике Каналы"""
        admin_channels_page.channels.open_the_channel_for_editing(
            text_row=data_channel['name']
        )
        data_channel['name'] = data_channel['name'][:-1] + '3'
        data_channel['naming'] = data_channel['naming'][:-1] + '4'
        admin_channels_page.channel_card.fill_required_fields(
            data_channel['name'],
            data_channel['naming'],
        )
        admin_channels_page.channel_card.click_save_channel_button()
        admin_channels_page.page.reload()
        admin_channels_page.channels.check_new_channel(data_channel)

    @staticmethod
    @pytest.mark.order(4)
    @pytest.mark.regress()
    @allure.title('Отмена редактирования записи в Справочнике Каналы')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story(jira.JIRA_LINK + 'MDP-416')
    @allure.testcase(case.ALLURE_LINK + '122448')
    def test_cancel_channel_editing(
            admin_channels_page: AdminOfficeChannelsPage,
            authorization_in_admin_office_with_token: str,
    ) -> None:
        """Отмена редактирование записи в Справочнике Каналы"""
        admin_channels_page.channels.open_the_channel_for_editing(
            text_row=data_channel['name']
        )
        data_channel['name'] = data_channel['name'][:-1] + '5'
        data_channel['naming'] = data_channel['naming'][:-1] + '6'
        admin_channels_page.channel_card.fill_required_fields(
            data_channel['name'],
            data_channel['naming'],
        )
        admin_channels_page.channel_card.cancel_editing()
        data_channel['name'] = data_channel['name'][:-1] + '3'
        data_channel['naming'] = data_channel['naming'][:-1] + '4'
        admin_channels_page.channels.check_new_channel(data_channel)
        delete_channel_by_code((data_channel['code']))
