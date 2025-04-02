from playwright.sync_api import Page
from admin_office.constants import LIMIT_OF_ROWS_ON_ONE_PAGE_IN_CHANNELS
from controller.button import Button
from controller.paging import Paging
from controller.table_new import Table
from controller.title import Title


class Channels:
    """Страница Каналы"""

    def __init__(self, page: Page) -> None:
        self.create_button = Button(
            page=page,
            locator="//button[.='Создать']",
            name='Создать канал',
        )
        self.table = Table(
            page=page,
            locator='table',
            name='Таблица каналов',
        )
        self.paging = Paging(
            page=page,
            locator="//div[@data-testid='channels_pagination']",
            name='Пейджинг',
        )
        self.title = Title(
            page=page,
            locator='h2',
            name='Заголовок',
        )

    def open_the_channel_creation_form(self) -> None:
        """Открыть форму создания канала"""
        self.create_button.click()

    def check_page_loading(self) -> None:
        """Проверить загрузку страницы"""
        self.title.should_have_text('Каналы')

    def check_quantity_channels(self, amount) -> None:
        """Проверяем количество записей в таблице"""
        count_row = (
            amount
            if amount < LIMIT_OF_ROWS_ON_ONE_PAGE_IN_CHANNELS
            else LIMIT_OF_ROWS_ON_ONE_PAGE_IN_CHANNELS
        )
        self.table.should_have_count_row(count_row=count_row)

    def check_transition_to_next_page(self, count_rows: int) -> None:
        """Проверяем, что при переходе на следующую страницу набор записей изменяется

        Args:
            count_rows: общее количество записей. Необходимо для проверки перехода на следующую страницу
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

    def check_new_channel(self, data_channel: dict) -> None:
        """Проверяем, что новый канал создан

        Args:
            data_channel данные канала
        """
        while self.paging.next_button.get_locator().is_enabled():
            self.table.should_be_visible()
            self.paging.go_to_next_page()

        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_channel['naming'],
            number_cell=0,
            check_text=data_channel['name'],
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_channel['naming'],
            number_cell=1,
            check_text=data_channel['code'],
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_channel['naming'],
            number_cell=2,
            check_text=data_channel['media_type'],
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_channel['naming'],
            number_cell=3,
            check_text='Да',
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_channel['code'],
            number_cell=4,
            check_text=data_channel['naming'],
        )

    def open_the_channel_for_editing_through_context_menu(
            self, text_row: str
    ) -> None:
        """Открыть форму редактирования канала через контекстное меню

        Args:
            text_row: текст строки
        """
        self.table.open_menu_action_in_row_by_contains_text(text_row)
        self.table.click_item_menu_action('Редактировать')

    def open_the_channel_for_editing(self, text_row: str) -> None:
        """Открыть форму редактирования канала

        Args:
            text_row: текст строки
        """
        self.table.cell_with_number_in_row_by_contains_text(
            text_row=text_row, number_cell=0
        ).locator('a').click()

    def click_to_next_page(self, how_much_clicks: int) -> None:
        start_page_number = 0
        while start_page_number < how_much_clicks:
            self.paging.go_to_next_page()
            start_page_number += 1
