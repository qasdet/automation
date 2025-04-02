import allure
import pytest

from admin_office.components.pages.users.users_page import AdminOfficeUsersPage
from admin_office.constants import LIMIT_OF_ROWS_ON_ONE_PAGE_IN_USERS
from admin_office.api_interactions.users.users_api_interactions import (
    get_count_of_users,
)
from admin_office.tests.api.users.data_make_for_users import (
    make_data_all_user_fields,
    make_the_expected_data_for_ui,
)
from db_stuff.db_interactions.users_db_interactions import (
    delete_user_by_id,
    get_user_by_login_and_phone_and_email,
)
from db_stuff.db_interactions.persons_db_interactions import (
    delete_person_by_id,
)


@pytest.fixture()
def life_cycle_of_the_user_with_all_field():
    data_user = make_data_all_user_fields()
    yield data_user
    user = get_user_by_login_and_phone_and_email(
        data_user['login'], data_user['phone'], data_user['email']
    )
    person = str(user.id)
    if person:
        delete_person_by_id(person)
    if user:
        delete_user_by_id(user.id)


@pytest.mark.usefixtures('authorization_in_admin_office_with_token')
class TestsUsers:
    @staticmethod
    @pytest.mark.smoke
    @allure.title('Страница Пользователи')
    def test_view_users(
            admin_users_page: AdminOfficeUsersPage,
            authorization_in_admin_office_with_token: str,
    ):
        """Страница Пользователи"""
        token = authorization_in_admin_office_with_token
        admin_users_page.go_to_users()
        count_all_rows = get_count_of_users(token)
        admin_users_page.users.check_quantity_users(count_all_rows)
        admin_users_page.users.check_transition_to_next_page(count_all_rows)
        count_rows_in_second_page = (
            count_all_rows
            if count_all_rows <= LIMIT_OF_ROWS_ON_ONE_PAGE_IN_USERS
            else count_all_rows - LIMIT_OF_ROWS_ON_ONE_PAGE_IN_USERS
        )
        admin_users_page.users.check_quantity_users(count_rows_in_second_page)

    @staticmethod
    @pytest.mark.smoke
    @allure.title("""Добавление пользователя""")
    def test_create_user(
            admin_users_page: AdminOfficeUsersPage,
            life_cycle_of_the_user_with_all_field,
    ):
        """Добавление пользователя"""
        data_user = life_cycle_of_the_user_with_all_field
        admin_users_page.side_bar.check_users_link()
        admin_users_page.users.open_the_user_creation_form()
        admin_users_page.card_user.fill_all_fields(**data_user)
        expected_data = make_the_expected_data_for_ui(data_user)
        admin_users_page.card_user.save_user()
        admin_users_page.reload()
        admin_users_page.users.check_new_user(expected_data)
