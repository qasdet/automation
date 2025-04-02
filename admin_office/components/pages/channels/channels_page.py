from playwright.sync_api import Page
from admin_office.components.base_page import BasePage
from admin_office.components.models.ui.channels.channel import Channels
from admin_office.components.models.ui.channels.channel_card import ChannelCard


class AdminOfficeChannelsPage(BasePage):
    """Каналы"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.channels = Channels(page)
        self.channel_card = ChannelCard(page)

    def go_to_channels(self) -> None:
        """Перейти в справочник Каналы"""
        self.side_bar.check_channels_link()
        self.channels.check_page_loading()
