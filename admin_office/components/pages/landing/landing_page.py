from playwright.sync_api import Page

from user_office.components.base_page import BasePage


class LandingPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page=page)

    def visit_landing_page(self, landing_page_url: str) -> None:
        """Переход на посадочную страницу"""
        self.visit(f'{landing_page_url}')
        self.page.wait_for_url(f'{landing_page_url}')
