from playwright.sync_api import Page
from controller.drop_down_list import DropDownList
from controller.button import Button
from controller.input import Input


class InstrumentsCard:
    """Модель страницы создания инструмента Постклик"""

    def __init__(self, page: Page) -> None:
        self.page = page

        self.tools_type_dropdown = DropDownList(
            page=page,
            locator="[data-testid='tools_type']",
            name='Тип',
        )
        self.tools_code_field = Input(
            page=page,
            locator="[data-testid='tools_code']",
            name='Код',
        )
        self.tools_can_auto_gather_switch = Button(
            page=page,
            locator="[data-testid='tools_can_auto_gather']",
            name='Автоматический сбор статистики',
        )
        self.tools_name_field = Input(
            page=page,
            locator="[data-testid='tools_name']",
            name='Наименование',
        )
        self.tools_short_name_field = Input(
            page=page,
            locator="[data-testid='tools_short_name']",
            name='Краткое наименование',
        )
        self.tools_url_field = Input(
            page=page,
            locator="[data-testid='tools_url']",
            name='URL',
        )
        self.tools_naming_field = Input(
            page=page,
            locator="[data-testid='tools_naming']",
            name='Нейминг',
        )
        self.tools_status_dropdown = DropDownList(
            page=page,
            locator="[data-testid='tools_status']",
            name='Статус',
        )
        self.tools_button_create = Button(
            page=page,
            locator="[data-testid='tools_button_create']",
            name='Создать',
        )
        self.tools_button_cancel = Button(
            page=page,
            locator="[data-testid='tools_button_cancel']",
            name='Отмена',
        )

    def fill_tools_type_dropdown(self, type_value="Верификатор") -> None:
        """ Выбирает тип инструменты. По умолчанию - 'Верификатор' """
        self.tools_type_dropdown.should_be_visible()
        self.tools_type_dropdown.select_item_by_text(type_value)

    def fill_tools_code_field(self, code_value: str) -> None:
        """ Заполняет поле 'Код' """
        self.tools_code_field.should_be_visible()
        self.tools_code_field.fill(code_value)

    def click_tools_can_auto_gather_switch(self) -> None:
        """ Включает/выключает 'Автоматический сбор статистики' """
        self.tools_can_auto_gather_switch.should_be_visible()
        self.tools_can_auto_gather_switch.click()

    def fill_tools_name_field(self, name_value: str) -> None:
        """ Заполняет поле 'Наименование' """
        self.tools_name_field.should_be_visible()
        self.tools_name_field.fill(name_value)

    def fill_tools_short_name_field(self, short_name_value: str) -> None:
        """ Заполняет поле 'Короткое наименование' """
        self.tools_short_name_field.should_be_visible()
        self.tools_short_name_field.fill(short_name_value)

    def fill_tools_url_field(self, url_value: str) -> None:
        """ Заполняет поле 'Урл' """
        self.tools_url_field.should_be_visible()
        self.tools_url_field.fill(url_value)

    def fill_tools_naming_field(self, naming_value: str) -> None:
        """ Заполняет поле 'Нейминг' """
        self.tools_naming_field.should_be_visible()
        self.tools_naming_field.fill(naming_value)

    def fill_tools_status_dropdown(self, status_value="Активный") -> None:
        """ Выбирает тип инструменты. По умолчанию - 'Активный' """
        self.tools_status_dropdown.should_be_visible()
        self.tools_status_dropdown.select_item_by_text(status_value)

    def click_create_button(self) -> None:
        """ Нажимает кнопку 'Создать' """
        self.tools_button_create.should_be_visible()
        self.tools_button_create.click()

    def click_cancel_button(self) -> None:
        """ Нажимает кнопку 'Отмена' """
        self.tools_button_cancel.should_be_visible()
        self.tools_button_cancel.click()
