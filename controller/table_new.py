import allure
from playwright.sync_api import Locator, expect

from controller.factory import AssertableMixin, ClickableMixin, Factory


class Table(ClickableMixin, AssertableMixin, Factory):
    """
    Компонент для работы с HTML таблицами (table/tbody).

    Наследует функциональность от ClickableMixin и AssertableMixin
    для выполнения действий и проверок над табличными данными.

    Использование:
        >>> table = Table(page, locator="[role='grid']", name="Таблица кампаний")
        >>> table.click_cell_in_row_by_num(0, 2).should_be_visible()

    Примеры:
        Клик по ячейке:
        >>> table.click_cell_by_text("Редактировать")

        Проверка количества строк:
        >>> table.should_have_row_count(10)
    """

    @property
    def type_of(self) -> str:
        return 'table'

    def tbody(self, **kwargs) -> Locator:
        """Тело таблицы"""
        return self.get_locator(**kwargs).locator(selector_or_locator='tbody')

    def cell_by_text(self, text_cell: str, **kwargs) -> Locator:
        """Ячейка в таблице по тексту (не привязана к строке)"""
        tbody: Locator = self.tbody(**kwargs)
        return tbody.get_by_role(role='cell', name=text_cell, exact=True)

    def cell_in_head(self, text_cell: str, **kwargs) -> Locator:
        """Ячейка в шапке таблицы по тексту"""
        table: Locator = self.get_locator(**kwargs)
        return table.locator(selector_or_locator='thead').get_by_role(
            role='cell', name=text_cell
        )

    def row_with_number(self, number_row: int, **kwargs) -> Locator:
        """Строка таблицы по порядковому номеру"""
        tbody: Locator = self.tbody(**kwargs)
        return tbody.get_by_role(role='row').nth(index=number_row)

    def row_by_contains_text(self, text_row: str, **kwargs) -> Locator:
        """Строка таблицы включает текст"""
        tbody: Locator = self.tbody(**kwargs)
        return tbody.get_by_role(role='row', name=text_row)

    def cell_with_text_in_row(
        self, number_row: int, text_cell: str, **kwargs
    ) -> Locator:
        """Ячейка c текстом в строке по порядковому номеру"""
        return self.row_with_number(
            number_row=number_row, **kwargs
        ).get_by_role(role='cell', name=text_cell, exact=True)

    def cell_with_number_in_row(
        self, number_row: int, number_cell: int, **kwargs
    ) -> Locator:
        """Ячейка по порядковому номеру в строке"""
        return (
            self.row_with_number(number_row=number_row, **kwargs)
            .get_by_role(role='cell')
            .nth(index=number_cell)
        )

    def cell_with_text_in_row_by_contains_text(
        self, text_row: str, text_cell: str, **kwargs
    ) -> Locator:
        """Ячейка c текстом в строке по указанному тексту"""
        return self.row_by_contains_text(
            text_row=text_row, **kwargs
        ).get_by_role(role='cell', name=text_cell, exact=True)

    def cell_with_number_in_row_by_contains_text(
        self, text_row: str, number_cell: int, **kwargs
    ) -> Locator:
        """Ячейка по порядковому номеру в строке"""
        return (
            self.row_by_contains_text(text_row=text_row, **kwargs)
            .get_by_role(role='cell')
            .nth(index=number_cell)
        )

    def button_menu_action_in_row(self, number_row: int, **kwargs) -> Locator:
        """Кнопка меню действий в строке"""
        return self.row_with_number(number_row=number_row, **kwargs).locator(
            selector_or_locator='button'
        )

    def button_menu_action_in_row_by_contains_text(
        self, text_row: str, **kwargs
    ) -> Locator:
        """Кнопка меню действий в строке"""
        return self.row_by_contains_text(text_row=text_row, **kwargs).locator(
            selector_or_locator='button'
        )

    def menu_action_in_table(self) -> Locator:
        """Контекстное меню действий над записью"""
        return self.page.locator("[role='dialog']")

    # === ASSERTION METHODS (FLUENT) ===

    def should_be_visible_cell_by_text(self, text_cell: str, **kwargs) -> 'Table':
        """Проверка что ячейка с текстом отображается"""
        expect(self.cell_by_text(text_cell=text_cell, **kwargs)).to_be_visible()
        return self

    def should_be_visible_row_by_contains_text(
        self, text_row: str, **kwargs
    ) -> 'Table':
        """Проверка что строка с текстом отображается"""
        expect(self.row_by_contains_text(text_row=text_row, **kwargs)).to_be_visible()
        return self

    def should_be_visible_cell_in_row(
        self, number_row: int, text_cell: str, **kwargs
    ) -> 'Table':
        """Проверка что ячейка с текстом в указанной строке отображается"""
        with allure.step(
            f'Checking cell with text "{text_cell}" in row {number_row}'
        ):
            expect(
                self.cell_with_text_in_row(
                    number_row=number_row, text_cell=text_cell, **kwargs
                )
            ).to_be_visible()
        return self

    def should_have_text_cell_in_row(
        self, number_row: int, number_cell: int, check_text: str, **kwargs
    ) -> 'Table':
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

    def should_be_visible_cell_in_row_by_contains_text(
        self, text_row: str, text_cell: str, **kwargs
    ) -> 'Table':
        """Проверка что ячейка с текстом в указанной строке отображается"""
        expect(
            self.cell_with_text_in_row_by_contains_text(
                text_row=text_row, text_cell=text_cell, **kwargs
            )
        ).to_be_visible()
        return self

    def should_have_text_cell_in_row_by_contains_text(
        self, text_row: str, number_cell: int, check_text: str, **kwargs
    ) -> 'Table':
        """Проверка что ячейка с номером в строке содержит текст"""
        with allure.step(
            f'Checking cell {number_cell} in row "{text_row}" has text "{check_text}"'
        ):
            expect(
                self.cell_with_number_in_row_by_contains_text(
                    text_row=text_row, number_cell=number_cell, **kwargs
                )
            ).to_have_text(expected=check_text)
        return self

    def should_be_visible_button_menu_action_in_row(
        self, number_row: int, **kwargs
    ) -> 'Table':
        """Проверка что кнопка меню действий в строке отображается"""
        expect(
            self.button_menu_action_in_row(number_row=number_row, **kwargs)
        ).to_be_visible()
        return self

    def should_be_visible_button_menu_action_in_row_by_contains_text(
        self, text_row: str, **kwargs
    ) -> 'Table':
        """Проверка что кнопка меню действий в строке отображается"""
        expect(
            self.button_menu_action_in_row_by_contains_text(text_row=text_row, **kwargs)
        ).to_be_visible()
        return self

    def should_be_visible_menu_action_in_table(self) -> 'Table':
        """Проверка что меню действий отображается"""
        expect(self.menu_action_in_table()).to_be_visible()
        return self

    def should_have_count_row(
        self, count_row: int, text_row: str = None, **kwargs
    ) -> 'Table':
        """Проверка количества записей в таблице"""
        with allure.step(
            f'Checking row count equals {count_row}'
        ):
            tbody: Locator = self.tbody(**kwargs)
            expect(
                actual=tbody.get_by_role(role='row', name=text_row)
            ).to_have_count(count=count_row)
        return self

    # === ACTION METHODS (FLUENT) ===

    def click_cell_in_row(
        self, number_row: int, text_cell: str, **kwargs
    ) -> 'Table':
        """Клик по ячейке в строке"""
        with allure.step(f'Clicking cell with text "{text_cell}" in row {number_row}'):
            self.cell_with_text_in_row(
                number_row=number_row, text_cell=text_cell, **kwargs
            ).click()
        return self

    def click_cell_in_row_by_num(
        self, number_row: int, number_cell: int, **kwargs
    ) -> 'Table':
        """Клик по ячейке с номером"""
        with allure.step(f'Clicking cell {number_cell} in row {number_row}'):
            self.cell_with_number_in_row(
                number_row=number_row, number_cell=number_cell, **kwargs
            ).click()
        return self

    def open_menu_action_in_row(self, number_row: int, **kwargs) -> 'Table':
        """Открыть меню действий в строке"""
        with allure.step(f'Opening menu action in row {number_row}'):
            self.button_menu_action_in_row(number_row=number_row, **kwargs).click()
            self.should_be_visible_button_menu_action_in_row(number_row=number_row, **kwargs)
        return self

    def open_menu_action_in_row_by_contains_text(
        self, text_row: str, **kwargs
    ) -> 'Table':
        """Открыть меню действий в строке"""
        with allure.step(f'Opening menu action in row "{text_row}"'):
            self.button_menu_action_in_row_by_contains_text(text_row=text_row, **kwargs).click()
            self.should_be_visible_button_menu_action_in_row_by_contains_text(text_row=text_row, **kwargs)
        return self

    def click_item_menu_action(self, text_item: str) -> 'Table':
        """Клик по действию в меню действий"""
        with allure.step(f'Clicking menu item "{text_item}"'):
            self.menu_action_in_table().get_by_text(
                text=text_item, exact=True
            ).click()
        return self

    def count_rows(self, text_row: str = None) -> int:
        """Количество записей в таблице"""
        return (
            self.get_locator()
            .locator(selector_or_locator='tbody')
            .get_by_role(role='row', name=text_row)
            .count()
        )

    def __repr__(self):
        return self.locator
