from playwright.sync_api import Page
from controller.button import Button
from controller.paging import Paging
from controller.table_new import Table
from controller.title import Title


class Sources:
    """Модель страницы Площадки"""

    def __init__(self, page: Page) -> None:
        self.page = page

        self.sources_button_create = Button(
            page=page,
            locator="[data-testid='sources_button_create']",
            name="Добавить продукт",
        )
        self.sources_title = Title(
            page=page,
            locator="[data-testid='dictionary-title-Площадки']",
            name="Заголовок",
        )
        self.sources_table = Table(
            page=page,
            locator="[data-testid='sources_table']",
            name="Таблица площадок",
        )
        self.sources_paging = Paging(
            page=page,
            locator="[data-testid='sources_pagination']",
            name="Пагинация",
        )
        self.sources_paging_prev_button = Paging(
            page=page,
            locator="[data-testid='sources_pagination_prev']",
            name="Кнопка пагинации 'Назад'",
        )
        self.sources_paging_next_button = Paging(
            page=page,
            locator="[data-testid='sources_pagination_next']",
            name="Кнопка пагинации 'Вперёд'",
        )

    def check_sources_page_loading(self) -> None:
        """Проверить загрузку страницы"""
        self.sources_title.should_have_text("Площадки")

    def click_create_new_source(self) -> None:
        """Открыть форму создания площадки"""
        self.sources_button_create.should_be_visible()
        self.sources_button_create.click()

    def check_quantity_of_sources(self, amount) -> None:
        """Проверяем количество записей в таблице"""
        self.sources_table.should_have_count_row(
            count_row=amount if amount <= 10 else 10
        )

    def click_prev_button(self) -> None:
        """Кликнуть по кнопке, чтобы перейти на предыдущую страницу"""
        self.sources_paging_prev_button.should_be_visible()
        self.sources_paging_prev_button.click()

    def click_next_button(self) -> None:
        """Кликнуть по кнопке, чтобы перейти на следующую страницу"""
        self.sources_paging_next_button.should_be_visible()
        self.sources_paging_next_button.click()

    def check_transition_to_next_page(self, count_rows: int) -> None:
        """Проверяем, что при переходе на следующую страницу набор записей изменяется

        Args:
            count_rows: общее количество записей. Необходимо для проверки перехода на следующую страницу
            Если записей < 10 переход не тестируем, т.к. в справочнике только 1 страница
        """
        if count_rows > 10:
            first_page_text = self.sources_table.inner_text()
            self.click_next_button()
            self.sources_table.should_be_visible()
            second_page_text = self.sources_table.inner_text()
            assert (
                    first_page_text != second_page_text
            ), 'Не смогли прейти на следующую страницу'

    def check_page_loading(self) -> None:
        """Проверить загрузку страницы"""
        self.sources_title.should_have_text('Площадки')

    def check_new_source(self, data_source: dict):
        """Проверить, что запись добавлена"""
        self.sources_table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_source['id'],
            number_cell=0,
            check_text=data_source['id'],
        )
        self.sources_table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_source['name'],
            number_cell=1,
            check_text=data_source['name'],
        )
        self.sources_table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_source['naming'],
            number_cell=2,
            check_text=data_source['naming'],
        )
        self.sources_table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_source['code'],
            number_cell=3,
            check_text=data_source['code'],
        )
        self.sources_table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_source['url'],
            number_cell=4,
            check_text=data_source['url'],
        )
