from playwright.sync_api import Page
from admin_office.components.base_page import BasePage
from admin_office.components.models.ui.instruments.instruments import Instruments
from admin_office.components.models.ui.instruments.instruments_card import InstrumentsCard


class AdminOfficeInstrumentsPage(BasePage):
    """Страница Инструменты"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.instruments = Instruments(page)
        self.instruments_card = InstrumentsCard(page)

    def go_to_instruments(self) -> None:
        """Перейти в справочник Инструменты"""
        self.side_bar.check_sources_category_link()
        self.side_bar.check_instruments_link()
        self.instruments.check_instruments_page_loading()
