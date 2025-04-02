from playwright.sync_api import Page

from admin_office.components.base_page import BasePage
from admin_office.components.models.ui.sources.sources import Sources
from admin_office.components.models.ui.sources.sources_card import SourcesCard


class AdminOfficeSourcesPage(BasePage):
    """Площадки"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.sources = Sources(page)
        self.sources_card = SourcesCard(page)

    def go_to_sources(self) -> None:
        """Перейти в справочник Площадки"""
        self.side_bar.check_sources_category_link()
        self.side_bar.check_sources_link()
        self.sources.check_page_loading()
