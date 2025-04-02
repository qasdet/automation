from playwright.sync_api import Page

from controller.button import Button
from controller.date_picker import DatePicker
from controller.drop_down_list import DropDownList
from controller.input import Input
from controller.title import Title
from user_office.components.models.ui.tv.tv_campaigns.dialog_conditions_tv import (
    ConditionsTVModal,
)
from user_office.components.models.ui.tv.tv_campaigns.dialog_market_targets_tv import (
    MarketTargetsTVModal,
)
from user_office.components.models.ui.tv.tv_campaigns.dialog_target_audience_tv import (
    TargetAudienceTVModal,
)


class CreateTVCampaign:
    """Модель страницы Создание TV кампании"""

    def __init__(self, page: Page) -> None:
        self.market_targets_dialog = MarketTargetsTVModal(page)
        self.target_audience_dialog = TargetAudienceTVModal(page)
        self.conditions_dialog = ConditionsTVModal(page)

        self.title = Title(
            page=page,
            locator="[data-testid='create_tv_campaign_title']",
            name='Заголовок',
        )

        self.status = Title(
            page=page,
            locator='.StatusLabel_label__xWQMV ',
            name='Статус тв кампании',
        )
        self.name_input = Input(
            page=page,
            locator="[data-testid='create_tv_campaign_name']",
            name='Название тв кампании',
        )
        self.date_start = DatePicker(
            page=page,
            locator="[data-testid='create_tv_campaign_date_start']",
            name='Начало периода',
        )
        self.date_end = DatePicker(
            page=page,
            locator="[data-testid='create_tv_campaign_date_end']",
            name='Конец периода',
        )
        self.client = DropDownList(
            page=page,
            locator="//div[@data-testid='create_tv_campaign_client']",
            name='Клиент',
        )
        self.brand = DropDownList(
            page=page,
            locator="//div[@data-testid='create_tv_campaign_brand']",
            name='Бренд',
        )
        self.product = DropDownList(
            page=page,
            locator="//div[@data-testid='create_tv_campaign_product']",
            name='Продукт',
        )
        self.create_draft_button = Button(
            page=page,
            locator="[data-testid='create_tv_campaign_draft_save_button']",
            name='Создать черновик',
        )
        self.create_tv_campaign_button = Button(
            page=page,
            locator="[data-testid='create_tv_campaign_save_button']",
            name='Создать тв кампанию',
        )

        self.market_targets_button = Button(
            page=page,
            locator="[data-testid='create_tv_campaign_market_targets__add_description']",
            name='Добавить описание Цели рекламной кампании',
        )
        self.market_targets_description = Title(
            page=page,
            locator="[data-testid='create_tv_campaign_market_targets__description']",
            name='Описание Цели рекламной кампании',
        )

        self.target_audience_button = Button(
            page=page,
            locator="[data-testid='create_tv_campaign_target_audience__add_description']",
            name='Добавить описание Целевая аудитория',
        )
        self.target_audience_description = Title(
            page=page,
            locator="[data-testid='create_tv_campaign_target_audience__description']",
            name='Описание Целевая аудитория',
        )

        self.conditions_button = Button(
            page=page,
            locator="[data-testid='create_tv_campaign_conditions__add_description']",
            name='Добавить описание Требования и ограничения',
        )
        self.conditions_description = Title(
            page=page,
            locator="[data-testid='create_tv_campaign_conditions__description']",
            name='Описание Требования и ограничения',
        )

    def check_page_loading(self) -> None:
        """Проверить загрузку страницы"""
        self.title.should_be_visible()

    def fill_for_market_targets(self, text: str) -> None:
        """Описание Целей рекламной кампании
        Args:
            text: цель рекламной кампании
        """
        self.market_targets_button.click()
        self.market_targets_dialog.fill_and_save_description(text)
        self.market_targets_description.should_have_text(text)

    def fill_for_target_audience(self, text: str) -> None:
        """Описание целевой аудитории
        Args:
            text: целевая аудитория
        """
        self.target_audience_button.click()
        self.target_audience_dialog.fill_and_save_description(text)
        self.target_audience_description.should_have_text(text)

    def fill_for_conditions(self, text: str) -> None:
        """Описание требований и ограничений
        Args:
            text: требования и ограничения
        """
        self.conditions_button.click()
        self.conditions_dialog.fill_and_save_description(text)
        self.conditions_description.should_have_text(text)

    def fill_fields(self, full_fields: bool = True, **kwargs: str) -> None:
        """Заполняем все поля ТВ кампании при создании
        Args:
            full_fields: True заполнить все поля,
                         False заполнить обязательные поля
            **kwargs: данные кампании
        """
        self.name_input.fill(kwargs.get('name'))
        self.date_start.click()
        self.date_start.fill(kwargs.get('date_start'))
        self.date_end.click()
        self.date_end.fill(kwargs.get('date_end'))
        self.client.select_item_by_text(
            f"{kwargs.get('client')} {kwargs.get('code_client')}"
        )
        self.brand.select_item_by_text(
            f"{kwargs.get('brand')} {kwargs.get('code_brand')}"
        )
        self.product.select_item_by_text(
            f"{kwargs.get('product')} {kwargs.get('code_product')}"
        )
        if full_fields:
            self.fill_for_market_targets(kwargs.get('market_targets'))
            self.fill_for_target_audience(kwargs.get('target_audience'))
            self.fill_for_conditions(kwargs.get('conditions'))

    def create_draft(self) -> None:
        """Сохранить черновик ТВ кампании"""
        self.create_draft_button.click()
        # self.status.should_have_text(DRAFT_STATUS)

    def create_tv_campaign(self) -> None:
        """Сохранить ТВ кампанию"""
        self.create_tv_campaign_button.click()
        self.create_tv_campaign_button.should_be_not_visible()

    def check_campaign_information_in_planning_status(self, **kwargs) -> None:
        """Проверяем, что информация о кампании
        совпадает с указанной (страница Подробнее о кампании /details)
        Args:
            **kwargs: ожидаеммая информация
        """
        # self.status.should_have_text(PLANNING_STATUS)
        self.check_campaign_information(**kwargs)

    def check_campaign_information_in_draft_status(self, **kwargs) -> None:
        # self.status.should_have_text(DRAFT_STATUS)
        self.check_campaign_information(**kwargs)

    def check_campaign_information(self, **kwargs):
        self.title.should_have_text(kwargs.get('name'))
        self.date_start.should_have_text(kwargs.get('date_start'))
        self.date_end.should_have_text(kwargs.get('date_end'))
        self.client.should_have_text(kwargs.get('client'))
        self.brand.should_have_text(kwargs.get('brand'))
        self.product.should_have_text(kwargs.get('product'))
        self.market_targets_description.should_have_text(
            kwargs.get('market_targets', '')
        )
        self.target_audience_description.should_have_text(
            kwargs.get('target_audience', '')
        )
        self.conditions_description.should_have_text(
            kwargs.get('conditions', '')
        )
