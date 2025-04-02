from playwright.sync_api import Page

from user_office.components.base_page import BasePage
from user_office.components.models.ui.tv.tv_campaigns.details_tv_campaings import (
    DetailsTVCampaign,
)


class DetailsTVCampaignPage(BasePage):
    """Страница детали ТВ кампании"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.details_tv_campaign = DetailsTVCampaign(page)
