from playwright.sync_api import Page

from user_office.components.base_page import BasePage


class CreateMediaplanPage(BasePage):
    def __init__(self, page: Page) -> None:
        super().__init__(page=page)
