import re

from playwright.sync_api import Page

from controller.button import Button
from controller.title import Title
from user_office.components.models.ui.tv.tv_mplan.tv_mplan_widget import (
    TVMplanWidget,
)
from user_office.constants import PATTERN_ID, PLANNING_STATUS, TV_TYPE


class TVCampaignCard:
    """Модель страницы ТВ кампании"""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.mpaln_widget = TVMplanWidget(page)
        self.name = Title(
            page=page,
            locator="[data-testid='campaign_tv_name']",
            name='Название тв кампании',
        )
        self.status = Title(
            page=page,
            locator="[data-testid='campaign_tv_status']",
            name='Статус',
        )
        self.date_created = Title(
            page=page,
            locator="[data-testid='campaign_tv_information']",
            name='Конец периода',
        )
        self.period = Title(
            page=page,
            locator="[data-testid='campaign_tv_period']",
            name='Период',
        )
        self.type_media = Title(
            page=page,
            locator="[data-testid='campaign_tv_type']",
            name='Тип кампании',
        )
        self.client = Title(
            page=page,
            locator="[data-testid='campaign_tv_client']",
            name='Клиент',
        )
        self.brand_product = Title(
            page=page,
            locator="[data-testid='campaign_tv_brands_and_products']",
            name='Бренд -> Продукт',
        )
        self.about_button = Button(
            page=page,
            locator="[data-testid='campaign_tv_about']",
            name='Подробнее о кампании',
        )

        self.create_mediaplan_button = Button(
            page=page,
            locator="[data-testid='campaign_tv_create_mediaplan']",
            name='Создать Медиаплан',
        )

    def check_campaign_info_in_planning_status(self, **kwargs) -> None:
        """Проверяем, что информация о кампании совпадает с указанной
        Args:
            **kwargs: ожидаеммая информация
        """
        self.status.should_have_text(PLANNING_STATUS)
        self.name.should_have_text(kwargs.get('name'))
        self.date_created.should_have_text(
            f"Создана {kwargs.get('date_start')}"
        )
        self.period.should_have_text(
            f"{kwargs.get('date_start')} - {kwargs.get('date_end')}"
        )
        self.type_media.should_have_text(TV_TYPE)
        self.client.should_have_text(kwargs.get('client'))
        self.brand_product.should_have_text(
            f"{kwargs.get('brand')} → {kwargs.get('product')}"
        )

    def open_about_campaign(self) -> None:
        """Открыть карточку подробнее о кампании"""
        self.about_button.click()
        self.about_button.should_be_not_visible()

    def get_id_from_url(self) -> str:
        """Получение id ТВ кампании из url"""
        pattern = re.compile(PATTERN_ID)
        tv_campaign_id = pattern.findall(self.page.url)
        if len(tv_campaign_id) > 0:
            return tv_campaign_id[0]
        else:
            raise Exception('id ТВ кампании не найдено')

    def open_card_create_mediaplan(self) -> None:
        """Открыть карточку создания медиаплана"""
        self.create_mediaplan_button.click()
