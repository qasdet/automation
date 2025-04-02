from playwright.sync_api import Page
from controller.title import Title
from controller.table_new import Table
from controller.button import Button


class Instruments:
    """Модель страницы Инструменты"""

    def __init__(self, page: Page) -> None:
        self.page = page

        self.instruments_title = Title(
            page=page,
            locator="[data-testid='dictionary-title-Инструменты']",
            name="Заголовок",
        )
        self.instruments_table = Table(
            page=page,
            locator="[data-testid='tools_table']",
            name="Таблица площадок",
        )
        self.tools_button_create = Button(
            page=page,
            locator="[data-testid='tools_button_create']",
            name="Создать",
        )
        self.tools_tracker_tab = Button(
            page=page,
            locator="[data-testid='tools_button_tracker_create']",
            name="Вкладка 'Трекер'",
        )
        self.tools_verifier_tab = Button(
            page=page,
            locator="[data-testid='tools_button_verifier_create']",
            name="Вкладка 'Верификатор'",
        )
        self.tools_postclick_tab = Button(
            page=page,
            locator="[data-testid='tools_button_postclick_create']",
            name="Вкладка 'Постклик'",
        )

    def check_instruments_page_loading(self) -> None:
        """Проверить загрузку страницы"""
        self.instruments_title.should_have_text("Инструменты")

    def click_tools_button_create(self) -> None:
        """ Нажать на кнопку 'Создать' """
        self.tools_button_create.should_be_visible()
        self.tools_button_create.click()

    def click_tracker_tab(self):
        """ Проверить, что вкладка 'Трекер' видна. Нажать на неё """
        self.tools_tracker_tab.should_be_visible()
        self.tools_tracker_tab.click()

    def click_verifier_tab(self):
        """ Проверить, что вкладка 'Верификатор' видна. Нажать на неё """
        self.tools_verifier_tab.should_be_visible()
        self.tools_verifier_tab.click()

    def click_postclick_tab(self):
        """ Проверить, что вкладка 'Постклик' видна. Нажать на неё """
        self.tools_postclick_tab.should_be_visible()
        self.tools_postclick_tab.click()

    def check_instruments_table(self, data_instruments: dict):
        """Проверить, что запись существует
            Args:
                data_instruments[id]: уникальный номер инструмента
                data_instruments[name]: название инструмента
                data_instruments[code]: код инструмента
                data_instruments[url]: url инструмента
        """
        self.instruments_table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_instruments['id'],
            number_cell=0,
            check_text=data_instruments['id'],
        )
        self.instruments_table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_instruments['name'],
            number_cell=1,
            check_text=data_instruments['name'],
        )
        self.instruments_table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_instruments['code'],
            number_cell=2,
            check_text=data_instruments['code'],
        )
        self.instruments_table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_instruments['url'],
            number_cell=3,
            check_text=data_instruments['url'],
        )
