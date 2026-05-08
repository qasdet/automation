import allure
from playwright.sync_api import Locator, expect

from controller.factory import AssertableMixin, ClickableMixin, Factory


class Grid(ClickableMixin, AssertableMixin, Factory):
    """
    Компонент для работы с GRID таблицами (role='grid').

    Наследует функциональность от ClickableMixin и AssertableMixin
    для выполнения действий и проверок над табличными данными.

    Использование:
        >>> grid = Grid(page, locator="[role='grid']", name="Таблица отчетности")
        >>> grid.should_have_row_count(5)

    Примеры:
        Клик по ячейке:
        >>> grid.click_cell_by_text("Итого")

        Проверка ячейки в строке:
        >>> grid.should_be_visible_cell_in_row(0, "Значение")
    """

    @property
    def type_of(self) -> str:
        return 'reporting_table'

    def grid(self, **kwargs) -> Locator:
        """Тело таблицы"""
        return self.get_locator(**kwargs).get_by_role(role='grid')

    def row_group(self, **kwargs) -> Locator:
        """Группа строк таблицы"""
        grid: Locator = self.grid(**kwargs)
        return grid.get_by_role(role='rowgroup')

    def row_header(self, **kwargs) -> Locator:
        """Группа строк заголовка таблицы"""
        row_group: Locator = self.row_group(**kwargs)
        return row_group.get_by_role(role='rowheader')

    def row(self, **kwargs) -> Locator:
        """Строка таблицы"""
        grid: Locator = self.grid(**kwargs)
        return grid.get_by_role(role='row')

    def cell_by_text(self, text_cell: str, **kwargs) -> Locator:
        """Ячейка в таблице по тексту (не привязана к строке)"""
        row: Locator = self.row(**kwargs)
        return row.get_by_role(role='gridcell', name=text_cell, exact=True)

    def row_with_number(self, number_row: int, **kwargs) -> Locator:
        """Строка таблицы по порядковому номеру"""
        grid: Locator = self.grid(**kwargs)
        return grid.get_by_role(role='row').nth(index=number_row)

    def cell_with_text_in_row(
        self, number_row: int, text_cell: str, **kwargs
    ) -> Locator:
        """Ячейка c текстом в строке по порядковому номеру"""
        return self.row_with_number(
            number_row=number_row, **kwargs
        ).get_by_role(role='gridcell', name=text_cell, exact=True)

    def cell_with_number_in_row(
        self, number_row: int, number_cell: int, **kwargs
    ) -> Locator:
        """Ячейка по порядковому номеру в строке"""
        return (
            self.row_with_number(number_row=number_row, **kwargs)
            .get_by_role(role='gridcell')
            .nth(index=number_cell)
        )

    def column_header_by_text(self, text_column: str, **kwargs) -> Locator:
        """Колонка в таблице по тексту заголовка"""
        row_header: Locator = self.row_header(**kwargs)
        return row_header.get_by_role(
            role='columnheader', name=text_column, exact=True
        )

    # === ASSERTION METHODS (FLUENT) ===

    def should_be_visible_cell_by_text(self, text_cell: str, **kwargs) -> 'Grid':
        """Проверка что ячейка с текстом отображается"""
        with allure.step(
            f'Checking cell with text "{text_cell}" is visible in {self.type_of} "{self.name}"'
        ):
            expect(self.cell_by_text(text_cell=text_cell, **kwargs)).to_be_visible()
        return self

    def should_be_visible_cell_in_row(
        self, number_row: int, text_cell: str, **kwargs
    ) -> 'Grid':
        """Проверка что ячейка с текстом в указанной строке отображается"""
        with allure.step(
            f'Checking cell with text "{text_cell}" in row {number_row} is visible'
        ):
            expect(
                self.cell_with_text_in_row(
                    number_row=number_row, text_cell=text_cell, **kwargs
                )
            ).to_be_visible()
        return self

    def should_have_text_cell_in_row(
        self, number_row: int, number_cell: int, check_text: str, **kwargs
    ) -> 'Grid':
        """Проверка что ячейка с номером в строке содержит текст"""
        with allure.step(
            f'Checking cell {number_cell} in row {number_row} has text "{check_text}"'
        ):
            expect(
                self.cell_with_number_in_row(
                    number_row=number_row, number_cell=number_cell, **kwargs
                )
            ).to_have_text(expected=check_text)
        return self

    def should_have_count_cell(
        self, count_cell: int, text_cell: str = None, **kwargs
    ) -> 'Grid':
        """Проверка количества ячеек с текстом"""
        with allure.step(
            f'Checking count of cells with text "{text_cell}" equals {count_cell}'
        ):
            expect(
                self.cell_by_text(text_cell=text_cell, **kwargs)
            ).to_have_count(count=count_cell)
        return self

    def should_have_row_count(self, count: int, **kwargs) -> 'Grid':
        """Проверка количества строк в таблице"""
        with allure.step(
            f'Checking row count in {self.type_of} "{self.name}" equals {count}'
        ):
            expect(self.row(**kwargs)).to_have_count(count=count)
        return self

    # === ACTION METHODS (FLUENT) ===

    def click_cell_in_row_by_num(
        self, number_row: int, number_cell: int, **kwargs
    ) -> 'Grid':
        """Клик по ячейке с номером"""
        with allure.step(
            f'Clicking cell {number_cell} in row {number_row}'
        ):
            self.cell_with_number_in_row(
                number_row=number_row, number_cell=number_cell, **kwargs
            ).click()
        return self

    def click_cell_by_text(self, text_cell: str, **kwargs) -> 'Grid':
        """Клик по ячейке с текстом"""
        with allure.step(f'Clicking cell with text "{text_cell}"'):
            self.cell_by_text(text_cell=text_cell, **kwargs).click()
        return self

    def double_click_cell_in_row(
        self, number_row: int, number_cell: int, **kwargs
    ) -> 'Grid':
        """Двойной клик по ячейке"""
        with allure.step(f'Double clicking cell {number_cell} in row {number_row}'):
            self.cell_with_number_in_row(
                number_row=number_row, number_cell=number_cell, **kwargs
            ).dblclick()
        return self

    def __repr__(self):
        return self.locator
