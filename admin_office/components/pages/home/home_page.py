from playwright.sync_api import Page

from admin_office.components.base_page import BasePage
from admin_office.components.models.ui.home.home import Home


class AdminOfficeHomePage(BasePage):
    """Стартовая страница Админ офис"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.home = Home(page)
