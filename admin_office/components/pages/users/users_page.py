from playwright.sync_api import Page

from admin_office.components.base_page import BasePage
from admin_office.components.models.ui.users.user_card import UserCard
from admin_office.components.models.ui.users.users import Users


class AdminOfficeUsersPage(BasePage):
    """Пользователи"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.users = Users(page)
        self.card_user = UserCard(page)

    def go_to_users(self):
        """Перейти на страницу Пользователи"""
        self.side_bar.check_users_link()
        self.users.check_page_loading()
