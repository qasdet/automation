import allure
import pytest

from admin_office.tests.api.users.data_make_for_users import (
    make_data_all_user_fields,
    make_the_expected_data_for_ui,
)
from db_stuff.db_interactions.users_db_interactions import delete_user_by_id
from db_stuff.db_interactions.persons_db_interactions import delete_person_by_id
from admin_office.constants import (
    USER_STATUS_NEW, USER_STATUS_BLOCKED
)
from helper.linkshort import JiraLink as jira
from user_office.components.pages.users.user_card_page import UserCardPage
from user_office.components.pages.users.users_page import UsersPage


@pytest.fixture()
def delete_user_by_id_in_organization(user_card_page):
    yield
    user_id = user_card_page.user_card.get_user_id()
    if user_id:
        delete_person_by_id(user_id)
        delete_user_by_id(user_id)


@pytest.mark.usefixtures('authorization_in_user_office')
class TestUserCreate:
    @staticmethod
    @pytest.mark.regress()
    @allure.title('Создать нового пользователя в user office')
    @allure.story(jira.JIRA_LINK + 'MDP-4143')
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_user(
        users_page: UsersPage,
        user_card_page: UserCardPage,
        delete_user_by_id_in_organization,
    ):
        data_user = make_data_all_user_fields()
        users_page.go_to_users()
        users_page.users_list.open_the_user_creation_form()
        user_card_page.user_card.check_the_card_is_visible()
        user_card_page.user_card.fill_all_fields(**data_user)
        user_card_page.user_card.save_user()
        expected_data = make_the_expected_data_for_ui(data_user)
        users_page.users_list.check_visible_new_user(**expected_data)
        users_page.users_list.open_the_user_for_editing(data_user['login'])
        user_card_page.user_card.check_the_card_is_visible()
        user_card_page.user_card.check_user_info(**expected_data)

    @staticmethod
    @pytest.mark.regress()
    @allure.title('Блокировка пользователя в user office')
    @allure.story(jira.JIRA_LINK + 'MDP-4145')
    @allure.severity(allure.severity_level.NORMAL)
    def test_blocked_user(
        users_page: UsersPage,
        user_card_page: UserCardPage,
        delete_user_by_id_in_organization,
    ):
        data_user = make_data_all_user_fields()
        users_page.go_to_users()
        users_page.users_list.open_the_user_creation_form()
        user_card_page.user_card.fill_all_fields(**data_user)
        user_card_page.user_card.save_user()
        users_page.users_list.open_the_user_for_editing(data_user['login'])
        user_card_page.user_card.blocked_user()
        data_user.update({'status': USER_STATUS_BLOCKED})
        users_page.users_list.check_visible_new_user(**data_user)
        users_page.users_list.open_the_user_for_editing(data_user['login'])
        user_card_page.user_card.check_the_card_is_visible()
        user_card_page.user_card.check_user_info(**data_user)

    @staticmethod
    @pytest.mark.regress()
    @allure.title('Редактирование пользователя в user office')
    @allure.story(jira.JIRA_LINK + 'MDP-4142')
    @allure.severity(allure.severity_level.NORMAL)
    def test_edited_user(
        users_page: UsersPage,
        user_card_page: UserCardPage,
        delete_user_by_id_in_organization,
    ):
        data_user = make_data_all_user_fields()
        users_page.go_to_users()
        users_page.users_list.open_the_user_creation_form()
        user_card_page.user_card.fill_all_fields(**data_user)
        user_card_page.user_card.save_user()
        users_page.users_list.open_the_user_for_editing(data_user['login'])
        data_user = make_data_all_user_fields()
        data_user.update({'status': USER_STATUS_NEW})
        user_card_page.user_card.fill_all_fields(**data_user)
        user_card_page.user_card.save_user()
        users_page.users_list.check_visible_new_user(**data_user)
        users_page.users_list.open_the_user_for_editing(data_user['login'])
        user_card_page.user_card.check_the_card_is_visible()
        user_card_page.user_card.check_user_info(**data_user)
