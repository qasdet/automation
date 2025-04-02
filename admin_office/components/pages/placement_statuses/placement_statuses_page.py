from playwright.sync_api import Page

from admin_office.components.base_page import BasePage
from admin_office.components.models.ui.placement_statuses.placement_statuses import (
    PlacementStatusesUI,
)


class AdminOfficePlacementStatusesPage(BasePage):
    """Статусы размещений"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.placement_statuses = PlacementStatusesUI(page)

    def go_to_placement_statuses(self):
        """Перейти на страницу Статусы размещений"""
        self.side_bar.check_placement_statuses_link()
        self.placement_statuses.check_page_loading()
