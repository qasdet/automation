from playwright.sync_api import Page

from controller.button import Button
from controller.drop_down_list import DropDownList
from controller.input import Input
from controller.title import Title


class BrandCard:
    """Модель страницы карточка бренда"""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.save_button = Button(
            page=page,
            locator="[data-testid='brand_card_save_button']",
            name='Сохранить',
        )
        self.cancel_button = Button(
            page=page,
            locator="[data-testid='brand_card_cancel_button']",
            name='Отмена',
        )
        self.organizations = DropDownList(
            page=page,
            locator="[data-testid='brand_card_organizations']",
            name='Организация',
        )
        self.brand_awareness = DropDownList(
            page=page,
            locator="//div[@data-testid='brand_card_awareness']",
            name='Известность бренда',
        )
        self.input_name = Input(
            page=page,
            locator="[data-testid='brand_card_name']",
            name='Наименование',
        )
        self.input_naming = Input(
            page=page,
            locator="[data-testid='brand_card_naming']",
            name='Нейминг',
        )
        self.title = Title(
            page=page,
            locator="[data-testid='brand_card_title']",
            name='Заголовок',
        )

    def fill_all_fields(
        self, name: str, naming: str, organization: str, brand_awareness: str
    ) -> None:
        """Заполяем все поля формы
        Args:
            name: поле Наименовани
            naming: поле Код
            organization: поле Клиенты
            brand_awareness: поле Известность для целевой аудитории
        """
        self.input_name.fill(name)
        self.input_naming.fill(naming)
        self.organizations.select_item_by_text(organization)
        self.brand_awareness.select_item_by_text(brand_awareness)

    def save_brand(self) -> None:
        """Сохранить бренд"""
        self.save_button.click()
        self.save_button.should_be_not_visible()
