from playwright.sync_api import Page

from admin_office.constants import LIMIT_OF_ROWS_ON_ONE_PAGE_IN_CLIENTS
from controller.button import Button
from controller.paging import Paging
from controller.table_new import Table
from controller.title import Title


class Clients:
    """Страница Клиенты"""

    def __init__(self, page: Page) -> None:
        self.create_button = Button(
            page=page,
            locator="[data-testid='clients_create_button']",
            name='Создать клиента',
        )
        self.table = Table(
            page=page,
            locator="[data-testid='clients_table']",
            name='Таблица клиентов',
        )
        self.paging = Paging(
            page=page,
            locator="//div[@data-testid='clients_pagination']",
            name='Пейджинг',
        )
        self.title = Title(
            page=page,
            locator="[data-testid='clients_title']",
            name='Заголовок',
        )

    def open_the_client_creation_form(self) -> None:
        """Открыть форму создания клиента"""
        self.create_button.click()

    def check_page_loading(self) -> None:
        """Проверить загрузку страницы"""
        self.title.should_have_text('Клиенты')

    def check_quantity_clients(self, amount) -> None:
        """Проверяем количество записей в таблице"""
        count_row = (
            amount
            if amount < LIMIT_OF_ROWS_ON_ONE_PAGE_IN_CLIENTS
            else LIMIT_OF_ROWS_ON_ONE_PAGE_IN_CLIENTS
        )
        self.table.should_have_count_row(count_row=count_row)

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

    def check_new_client(self, data_client: dict) -> None:
        """Проверяем, что новый клиент создан

        Args:
            data_client данные клиента
        """
        self.table.should_be_visible()
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_client['naming'],
            number_cell=1,
            check_text=data_client['naming'],
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_client['naming'],
            number_cell=2,
            check_text=data_client['name'],
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_client['naming'],
            number_cell=3,
            check_text=data_client['organization'],
        )
