from playwright.sync_api import Page

from user_office.components.base_page import BasePage
from user_office.components.models.ui.tv.tv_campaigns.create_tv_campaings import (
    CreateTVCampaign,
)


class CreateTVCampaignPage(BasePage):
    """Страница Создание TV кампании"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.create_tv_campaign = CreateTVCampaign(page)
