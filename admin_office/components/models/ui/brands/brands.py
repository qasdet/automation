from playwright.sync_api import Page

from admin_office.constants import LIMIT_OF_ROWS_ON_ONE_PAGE_IN_BRANDS
from controller.button import Button
from controller.paging import Paging
from controller.table_new import Table
from controller.title import Title


class Brands:
    """Модель страницы брендов"""

    def __init__(self, page: Page) -> None:
        self.page = page

        self.create_button = Button(
            page=page,
            locator="[data-testid='brands_create_button']",
            name='Добавить организацию',
        )
        self.table = Table(
            page=page,
            locator="[data-testid='brands_table']",
            name='Таблица брендов',
        )
        self.paging = Paging(
            page=page,
            locator="//div[@data-testid='brands_pagination']",
            name='Пейджинг',
        )
        self.title = Title(
            page=page, locator="[data-testid='brands_title']", name='Заголовок'
        )

    def open_the_brand_creation_form(self):
        """Открыть форму создания бренда"""
        self.create_button.click()

    def check_page_loading(self):
        """Проверить загрузку страницы"""
        self.title.should_have_text('Бренды')

    def check_quantity_brands(self, amount) -> None:
        """Проверяем количество записей в таблице"""
        count_row = (
            amount
            if amount < LIMIT_OF_ROWS_ON_ONE_PAGE_IN_BRANDS
            else LIMIT_OF_ROWS_ON_ONE_PAGE_IN_BRANDS
        )
        self.table.should_have_count_row(count_row=count_row)

    def check_transition_to_next_page(self, count_rows: int) -> None:
        """Проверяем, что при переходе на следующую страницу набор записей изменяется

        Args:
            count_rows: общее количество записей.
            Необходимо для проверки перехода на следующую страницу
            Если записей < 20 переход не тестируем, т.к. в справочнике только 1 страница
        """
        if count_rows > 20:
            first_page_text = self.table.inner_text()
            self.paging.go_to_next_page()
            self.table.should_be_visible()
            second_page_text = self.table.inner_text()
            assert (
                first_page_text != second_page_text
            ), 'Не смогли прейти на следующую страницу'

    def check_new_brand(self, data_brand: dict):
        """Проверяем, что запись добавлена
            Примечение: Для теста запись добавляется первой в списке. Проверяем, по 4-м значениям
            (наименование, код, клиент, известность)
        Args:
            data_brand данные о бренде
        """
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_brand['naming'],
            number_cell=1,
            check_text=data_brand['name'],
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_brand['naming'],
            number_cell=2,
            check_text=data_brand['organization'],
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_brand['naming'],
            number_cell=3,
            check_text=data_brand['naming'],
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_brand['naming'],
            number_cell=4,
            check_text=data_brand['brand_awareness'],
        )
