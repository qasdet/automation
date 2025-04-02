from playwright.sync_api import Page

from controller.button import Button
from controller.drop_down_list import DropDownList
from controller.input import Input
from controller.title import Title


class ClientCard:
    """Страница Карточка Клиента"""

    def __init__(self, page: Page) -> None:
        self.save_button = Button(
            page=page,
            locator="[data-testid='client_card_save_button']",
            name='Сохранить',
        )
        self.cancel_button = Button(
            page=page,
            locator="[data-testid='client_card_cancel_button']",
            name='Отмена',
        )
        self.title = Title(
            page=page,
            locator="[data-testid='client_card_title']",
            name='Заголовок',
        )
        self.input_name = Input(
            page=page,
            locator="[data-testid='client_card_name']",
            name='Название',
        )
        self.input_naming = Input(
            page=page, locator="[data-testid='client_card_naming']", name='Код'
        )
        self.organization = DropDownList(
            page=page,
            locator="[data-testid='client_card_organizations']",
            name='Организация',
        )

    def fill_all_fields(
        self, name: str, naming: str, full_name: str, inn: str, kpp: str, organization: str,
    ) -> None:
        """Заполняем все поля формы
        Args:
            name: Наименование
            naming: Нейминг
            full_name: Полное название организации (сейчас не используется, так как нет поля в UI)
            inn: ИНН организации (сейчас не используется, так как нет поля в UI)
            kpp: КПП организации (сейчас не используется, так как нет поля в UI)
            organization: Организация
        """
        self.input_name.fill(name)
        self.input_naming.fill(naming)
        self.organization.select_item_by_text(name_item=organization)

    def save_client(self) -> None:
        """Сохранить организацию"""
        self.save_button.click()
        self.save_button.should_be_not_visible()
