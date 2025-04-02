from playwright.sync_api import Page

from user_office.components.base_page import BasePage


class MediaPlanProfilePage(BasePage):
    """СТраница профиля пользователя"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
