from playwright.sync_api import Page

from admin_office.components.base_page import BasePage
from admin_office.components.models.ui.clients.client_card import ClientCard
from admin_office.components.models.ui.clients.clients import Clients


class AdminOfficeClientsPage(BasePage):
    """Клиенты"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.clients = Clients(page)
        self.client_card = ClientCard(page)

    def go_to_clients(self) -> None:
        """Перейти в справочник Клиенты"""
        self.side_bar.check_clients_link()
        self.clients.check_page_loading()
