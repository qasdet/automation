from playwright.sync_api import Page

from controller.link import Link
from user_office.components.models.ui.profile_modal.profile_modal import (
    ProfileModal,
)


class Navbar:
    """navbar в user office"""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.profile_modal = ProfileModal(page)
        self.campaigns = Link(
            page, locator="//a[.='Кампании']", name='Кампании'
        )
        self.references = Link(
            page, locator="//a[.='Справочники']", name='Справочники'
        )
        self.about_services = Link(
            page, locator="//a[.='О сервисе']", name='О сервиса'
        )
        self.support = Link(
            page, locator="//a[.='Поддержка']", name='Поддержка'
        )

    def visit_campaigns(self):
        # self.campaigns.should_be_visible()
        self.campaigns.click()

    def visit_references(self):
        # self.references.should_be_visible()
        self.references.click()

    def visit_about_services(self):
        # self.about_services.should_be_visible()
        self.about_services.click()

    def visit_support(self):
        # self.support.should_be_visible()
        self.support.click()

    def profile_open(self):
        self.profile_modal.modal_open()

    def profile_user(self):
        self.profile_modal.profile_user_modal()

    def profile_org(self):
        self.profile_modal.profile_organization_modal()
