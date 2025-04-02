from playwright.sync_api import Page

from admin_office.constants import LIMIT_OF_ROWS_ON_ONE_PAGE_IN_ORGANIZATIONS
from controller.button import Button
from controller.paging import Paging
from controller.table_new import Table
from controller.title import Title


class Organizations:
    """Модель страницы организации"""

    def __init__(self, page: Page) -> None:
        self.page = page

        self.create_button = Button(
            page=page,
            locator="[data-testid='organizations_create_button']",
            name='Добавить организацию',
        )
        self.filter_button = Button(
            page=page,
            locator="[data-testid='organizations_open_filter_button']",
            name='Открыть-Закрыть фильтры',
        )
        self.clear_filter_button = Button(
            page=page,
            locator="[data-testid='organizations_filter_reset']",
            name='Сбросить фильтры',
        )
        self.table = Table(
            page=page,
            locator="[data-testid='organizations_table']",
            name='Таблица организаций',
        )
        self.title = Title(
            page=page,
            locator="[data-testid='organizations_title']",
            name='Заголовок',
        )

        self.paging = Paging(
            page=page,
            locator="//div[@data-testid='organizations_pagination']",
            name='Пейджинг',
        )

    def open_the_organization_creation_form(self) -> None:
        """Открыть форму создания организации"""
        self.create_button.click()

    def check_page_loading(self) -> None:
        """Проверить загрузку страницы"""
        self.title.should_have_text('Организации')

    def check_table_loading(self) -> None:
        """Проверить загрузку таблицы"""
        self.table.should_be_visible()

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

    def check_quantity_organizations(self, amount) -> None:
        """Проверяем количество записей в таблице"""
        count_row = (
            amount
            if amount < LIMIT_OF_ROWS_ON_ONE_PAGE_IN_ORGANIZATIONS
            else LIMIT_OF_ROWS_ON_ONE_PAGE_IN_ORGANIZATIONS
        )
        self.table.should_have_count_row(count_row=count_row)

    def check_new_organization(self, data_organization: dict) -> None:
        """Проверить, что запись добавлена"""
        self.table.should_be_visible()
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_organization['inn'],
            number_cell=0,
            check_text=data_organization['fullName'],
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_organization['inn'],
            number_cell=1,
            check_text=data_organization['inn'],
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_organization['inn'],
            number_cell=2,
            check_text=data_organization['kpp'],
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_organization['inn'],
            number_cell=3,
            check_text=data_organization['address'],
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_organization['inn'],
            number_cell=4,
            check_text=data_organization['status'],
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_organization['inn'],
            number_cell=5,
            check_text=data_organization['registered_at'],
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_organization['inn'], number_cell=6, check_text=''
        )
