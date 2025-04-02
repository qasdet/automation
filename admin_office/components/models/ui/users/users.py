from playwright.sync_api import Page
from admin_office.constants import LIMIT_OF_ROWS_ON_ONE_PAGE_IN_USERS
from controller.button import Button
from controller.paging import Paging
from controller.table_new import Table
from controller.title import Title


class Users:
    """Модель страницы пользователей"""

    def __init__(self, page: Page) -> None:
        self.create_button = Button(
            page=page,
            locator="[data-testid='users_create_button']",
            name='Добавить организацию',
        )
        self.table = Table(
            page=page,
            locator="[data-testid='users_table']",
            name='Таблица пользователей',
        )
        self.paging = Paging(
            page=page,
            locator="//div[@data-testid='users_pagination']",
            name='Пейджинг',
        )
        self.title = Title(
            page=page, locator="[data-testid='users_title']", name='Заголовок'
        )

    def open_the_user_creation_form(self) -> None:
        """Открыть форму создания пользователя"""
        self.create_button.click()

    def check_page_loading(self) -> None:
        """Проверить загрузку страницы"""
        self.title.should_have_text('Пользователи')

    def check_quantity_users(self, amount) -> None:
        """Проверяем количество записей в таблице"""
        count_row = (
            amount
            if amount < LIMIT_OF_ROWS_ON_ONE_PAGE_IN_USERS
            else LIMIT_OF_ROWS_ON_ONE_PAGE_IN_USERS
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

    def check_new_user(self, data_user: dict) -> None:
        """Проверяем, что новый пользователь отображается в списке
            Примечание: В Пользователях сортировка в списке выполняется по id,
            поэтому нужно перейти к последней странице.
            Последняя запись в списке - это новый пользователь

        Args:
            data_user данные пользователя
        """

        while self.paging.next_button.get_locator().is_enabled():
            self.table.should_be_visible()
            self.paging.go_to_next_page()

        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_user['login'],
            number_cell=1,
            check_text=data_user['login'],
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_user['login'],
            number_cell=2,
            check_text=data_user['surname'],
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_user['login'],
            number_cell=3,
            check_text=data_user['name'],
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_user['login'],
            number_cell=4,
            check_text=data_user['middle_name'],
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_user['login'],
            number_cell=5,
            check_text=data_user['email'],
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_user['login'],
            number_cell=6,
            check_text=data_user['status'],
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_user['login'],
            number_cell=7,
            check_text=data_user['phone'],
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_user['login'],
            number_cell=8,
            check_text=data_user['role'],
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_user['login'],
            number_cell=9,
            check_text=data_user['organization'],
        )
