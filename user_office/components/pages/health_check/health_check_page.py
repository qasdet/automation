from playwright.sync_api import Page

from user_office.components.base_page import BasePage
from user_office.components.models.ui.health_check.health_user_office import (
    HealthUserOffice,
)


class HealthCheckPage(BasePage):
    """Страница для теста health check"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.health_user_office = HealthUserOffice(page)
