from playwright.sync_api import Page

from controller.button import Button
from controller.title import Title
from user_office.constants import DRAFT_STATUS


class TVMplanWidget:
    """Модель виджета медиаплана в карточке ТВ кампании"""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.status = Title(
            page=page,
            locator="[data-testid='campaign_tv_mplan_status']",
            name='Статус',
        )
        self.name = Title(
            page=page,
            locator="[data-testid='campaign_tv_mplan_name']",
            name='Продукт',
        )
        self.info = Title(
            page=page,
            locator="[data-testid='campaign_tv_mplan_information']",
            name='Данные о медиаплане',
        )
        self.goal = Title(
            page=page,
            locator="[data-testid='campaign_tv_mplan_goal']",
            name='Цель',
        )
        self.budget = Title(
            page=page,
            locator="[data-testid='campaign_tv_mplan_budget']",
            name='Бюджет',
        )
        self.channels = Title(
            page=page,
            locator="[data-testid='campaign_tv_mplan_channels']",
            name='Каналы',
        )
        self.tune_button = Button(
            page=page,
            locator="[data-testid='campaign_tv_mplan_tune_button']",
            name='Настроить',
        )

    def open_tv_mplan_card(self) -> None:
        """Открыть карточку ТВ медиа плана"""
        self.tune_button.click()

    def check_information_about_mplan(self, **kwargs) -> None:
        self.status.should_have_text(DRAFT_STATUS)
        self.name.should_have_text(kwargs.get('product'))
        # self.info.should_have_text(
        #     f"Медиаплан №0 | {kwargs.get('client')} | {kwargs.get('brand')}"
        # )
        self.goal.should_have_text(kwargs.get('goals'))
