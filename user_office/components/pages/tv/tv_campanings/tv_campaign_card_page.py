from playwright.sync_api import Page

from user_office.components.base_page import BasePage
from user_office.components.models.ui.tv.tv_campaigns.tv_campaign_card import (
    TVCampaignCard,
)


class TVCampaignCardPage(BasePage):
    """Страница ТВ кампаний"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.tv_campaign_card = TVCampaignCard(page)
