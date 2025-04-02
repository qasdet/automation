from playwright.sync_api import Page

from controller.table_new import Table
from controller.title import Title


class PlacementStatusesUI:
    """Модель страницы Статусы размещений"""

    def __init__(self, page: Page) -> None:
        self.page = page

        self.table = Table(
            page=page,
            locator='table',
            name='Таблица Статусы размещений',
        )
        self.title = Title(
            page=page,
            locator='h2',
            name='Заголовок',
        )

    def check_table_loading(self) -> None:
        """Проверить загрузку таблицы"""
        self.table.should_be_visible()

    def check_page_loading(self) -> None:
        """Проверить загрузку страницы"""
        self.title.should_have_text('Статусы размещений')
