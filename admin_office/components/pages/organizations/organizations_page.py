from playwright.sync_api import Page

from admin_office.components.base_page import BasePage
from admin_office.components.models.ui.organizations.organization_card import (
    OrganizationCard,
)
from admin_office.components.models.ui.organizations.organizations import (
    Organizations,
)


class AdminOfficeOrganizationsPage(BasePage):
    """Организации"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.organizations = Organizations(page)
        self.card_organization = OrganizationCard(page)

    def go_to_organizations(self):
        """Перейти на страницу Организации"""
        self.side_bar.check_organizations_link()
        self.organizations.check_page_loading()
