from playwright.sync_api import Page

from admin_office.components.base_page import BasePage
from admin_office.components.models.ui.authorization.form_authorization import (
    FormAuthorization,
)


class AdminOfficeAuthorizationPage(BasePage):
    """Авторизация"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.authorization = FormAuthorization(page)
