from playwright.sync_api import Page

from user_office.components.base_page import BasePage
from user_office.components.models.ui.authorization.authorization import (
    AuthorizeUserOffice,
)


class AuthorizationPage(BasePage):
    """Страница авторизации в user office"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.authorize = AuthorizeUserOffice(page)
