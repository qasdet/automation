from playwright.sync_api import Page

from controller.alphanumeric_element import AlphanumericElement
from controller.context_menu import ContextMenu
from controller.factory import Factory


class Cell(AlphanumericElement):
    @property
    def type_of(self) -> str:
        return 'cell'

    def __init__(self, page: Page, locator: str, name: str) -> None:
        super().__init__(page=page, locator=locator, name=name)


class Row(AlphanumericElement):
    @property
    def type_of(self) -> str:
        return 'row'

    def __init__(self, page: Page, locator: str, name: str) -> None:
        super().__init__(page=page, locator=locator, name=name)

        self.cell = Cell(
            page=page,
            locator=self.locator + '//td[{number_cell}]',
            name='Ячейка',
        )
        self.menu_action = AlphanumericElement(
            page=page,
            locator=self.locator + '//mts-button',
            name='Кнопка Меню',
        )
        self.context_menu = ContextMenu(
            page=page,
            locator="//mts-contextify[@visible='true']",
            name='Меню действий',
        )

    def open_menu_action(self, **kwargs) -> None:
        self.menu_action.click(**kwargs)
        self.context_menu.should_be_visible()

    def count_cells(self, **kwargs) -> int:
        """Количество ячеек в строке

        Returns:
            Количество ячеек
        """
        return self.get_locator(**kwargs).get_by_role(role='cell').count()


class HeadRow(Row):
    @property
    def type_of(self) -> str:
        return 'row'

    def __init__(self, page: Page, locator: str, name: str) -> None:
        super().__init__(page=page, locator=locator, name=name)

        self.cell = Cell(
            page=page,
            locator=self.locator + '//th[{number_cell}]',
            name='Ячейка',
        )


class TableBase(Factory):
    @property
    def type_of(self) -> str:
        return 'table'

    def __init__(self, page: Page, locator: str, name: str) -> None:
        super().__init__(page=page, locator=locator, name=name)

        self.row = Row(
            page=page,
            locator=self.locator
            + "//tbody//tr[td//text()[contains(., '{contains_text}')]][{number_row}]",
            name='Строка',
        )

        self.head_row = HeadRow(
            page=page,
            locator=self.locator + '//thead//tr',
            name='Шапка таблицы',
        )

    def count_rows(self, contains_text: str = None) -> int:
        """Количество записей (без заголовка)

        Args:
            contains_text текст, который содержат искомые записи, если None возвращаем все записи в таблице
        Returns:
            Количество записей
        """
        return (
            self.get_locator()
            .locator(selector_or_locator='tbody')
            .get_by_role(role='row', name=contains_text)
            .count()
        )


    def __repr__(self):
        return self.locator