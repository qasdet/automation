from playwright.sync_api import Page

from user_office.components.base_page import BasePage
from user_office.components.models.ui.tv.tv_campaigns.tv_campaigns import (
    TVCampaigns,
)


class TVCampaignsPage(BasePage):
    """Страница Карточка ТВ кампании"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.tv_campaigns = TVCampaigns(page)

    def check_loading_page(self) -> None:
        """Проверка загрузки страницы"""
        self.tv_campaigns.tabbar.should_be_active_tab_by_text(
            'Digital кампании'
        )

    def visit_tv_campaigns_page(self, office_base_url: str) -> None:
        """Переход на страницу ТВ кампании"""
        self.visit(f'{office_base_url}campaigns/tv/')
        self.tv_campaigns.create_button.should_be_visible()
        # TODO расскипать после решения бага MDP-3593
        # self.page.wait_for_timeout(15000)
        # self.tv_campaigns.table.should_be_visible()
