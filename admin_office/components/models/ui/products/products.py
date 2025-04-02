from playwright.sync_api import Page
from controller.button import Button
from controller.paging import Paging
from controller.table_new import Table
from controller.title import Title


class Products:
    """Модель страницы продукты"""

    def __init__(self, page: Page) -> None:
        self.page = page

        self.create_button = Button(
            page=page,
            locator="[data-testid='products_create_button']",
            name='Добавить продукт',
        )

        self.table = Table(
            page=page,
            locator="[data-testid='products_table']",
            name='Таблица продуктов',
        )
        self.paging = Paging(
            page=page,
            locator="//div[@data-testid='products_pagination']",
            name='Пейджинг',
        )
        self.title = Title(
            page=page,
            locator="[data-testid='products_title']",
            name='Заголовок',
        )
        self.dialog_confirm_button = Button(
            page=page,
            locator="[data-testid='dialog_confirm']",
            name="Ok"
        )
        self.dialog_cancel_button = Button(
            page=page,
            locator="[data-testid='dialog_cancel']",
            name="Отмена"
        )

    def click_dialog_confirm_button(self) -> None:
        """Нажать кнопку 'Ok' в модальном окне"""
        self.dialog_confirm_button.should_be_visible()
        self.dialog_confirm_button.click()

    def click_dialog_cancel_button(self) -> None:
        """Нажать кнопку 'Отмена' в модальном окне"""
        self.dialog_cancel_button.should_be_visible()
        self.dialog_cancel_button.click()

    def check_page_loading(self) -> None:
        """Проверить загрузку страницы"""
        self.title.should_have_text('Продукты')

    def open_the_product_creation_form(self) -> None:
        """Открыть форму создания продукта"""
        self.create_button.click()

    def check_quantity_products(self, amount) -> None:
        """Проверяем количество записей в таблице"""
        self.table.should_have_count_row(
            count_row=amount if amount <= 10 else 10
        )

    def check_transition_to_next_page(self, count_rows: int) -> None:
        """Проверяем, что при переходе на следующую страницу набор записей изменяется

        Args:
            count_rows: общее количество записей.
            Необходимо для проверки перехода на следующую страницу
            Если записей < 10 переход не тестируем, т.к. в справочнике только 1 страница
        """
        if count_rows > 10:
            first_page_text = self.table.inner_text()
            self.paging.go_to_next_page()
            self.table.should_be_visible()
            second_page_text = self.table.inner_text()
            assert (
                first_page_text != second_page_text
            ), 'Не смогли прейти на следующую страницу'

    def check_new_product(self, data_product: dict):
        """Проверить, что запись добавлена"""
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_product['naming'],
            number_cell=1,
            check_text=data_product['name'],
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_product['naming'],
            number_cell=3,
            check_text=data_product['naming'],
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_product['organization'],
            number_cell=4,
            check_text=data_product['organization'],
        )
