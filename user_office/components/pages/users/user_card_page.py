from playwright.sync_api import Page

from user_office.components.base_page import BasePage
from user_office.components.models.ui.users.user_card import UserCard


class UserCardPage(BasePage):
    """Страница Пользователей в User Office"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.user_card = UserCard(page)
