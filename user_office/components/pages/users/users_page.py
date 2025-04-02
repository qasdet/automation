from playwright.sync_api import Page

from user_office.components.base_page import BasePage
from user_office.components.models.ui.users.users_list import UsersList


class UsersPage(BasePage):
    """Страница Пользователей в User Office"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.users_list = UsersList(page)

    def go_to_users(self) -> None:
        """Перейти на страницу Пользователи"""
        self.navbar.profile_modal.modal_open()
        self.navbar.profile_modal.go_to_users()
        self.users_list.table.should_be_visible()
