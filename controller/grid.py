import allure
from playwright.sync_api import Locator, expect

from controller.factory import Factory


class Grid(Factory):
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
        """Группа строк таблицы"""
        row_group: Locator = self.row_group(**kwargs)
        return row_group.get_by_role(role='rowheader')

    def row(self, **kwargs) -> Locator:
        """Строка таблицы"""
        grid: Locator = self.grid(**kwargs)
        return grid.get_by_role(role='row')

    def cell_by_text(self, text_cell: str, **kwargs) -> Locator:
        """Ячейка в таблице по тексту (не привязана к строке)
        Args:
            text_cell: текст ячейки
            Return:
                Элемент типа Locator
        """
        row: Locator = self.row(**kwargs)
        return row.get_by_role(role='gridcell', name=text_cell, exact=True)

    def row_with_number(self, number_row: int, **kwargs) -> Locator:
        """Строка таблицы по порядковому номеру
        Args:
            number_row: порядковый номер строки
        Return:
            Элемент типа Locator
        """

        grid: Locator = self.grid(**kwargs)
        return grid.get_by_role(role='row').nth(index=number_row)

    def cell_with_text_in_row(
        self, number_row: int, text_cell: str, **kwargs
    ) -> Locator:
        """Ячейка c текстом в строке по порядковому номеру
        Args:
            number_row: порядковый номер строки
            text_cell: текст ячейки
        Return:
            Элемент типа Locator
        """

        return self.row_with_number(
            number_row=number_row, **kwargs
        ).get_by_role(role='gridcell', name=text_cell, exact=True)

    def cell_with_number_in_row(
        self, number_row: int, number_cell: int, **kwargs
    ) -> Locator:
        """Ячейка по порядковому номеру в строке
        Args:
            number_row: порядковый номер строки
            number_cell: порядковый номер ячейки
        Return:
            Элемент типа Locator
        """
        return (
            self.row_with_number(number_row=number_row, **kwargs)
            .get_by_role(role='gridcell')
            .nth(index=number_cell)
        )

    # Методы для взаимодействия с таблицей
    def should_be_visible_cell_by_text(self, text_cell: str, **kwargs) -> None:
        """Проверка, что ячейка с текстом  отображается (не привязана к строке)
        Args:
            text_cell: текст ячейки
        """
        expect(
            actual=self.cell_by_text(text_cell=text_cell, **kwargs)
        ).to_be_visible()

    def should_be_visible_cell_in_row(
        self, number_row: int, text_cell: str, **kwargs
    ) -> None:
        """Проверка, что ячейка с текстом в указанной строке отображается
        Args:
            number_row: порядковый номер строки
            text_cell: текст ячейки
        """
        with allure.step(
            title=f'Проверка, что ячейки с текстом {text_cell} '
            f'в строке под номером {number_row} отображается'
        ):
            expect(
                actual=self.cell_with_text_in_row(
                    number_row=number_row, text_cell=text_cell, **kwargs
                )
            ).to_be_visible()

    def should_have_text_cell_in_row(
        self, number_row: int, number_cell, check_text: str, **kwargs
    ) -> None:
        """Проверка, что ячейка с порядковым номером
        в указанной строке отображается
        Args:
            number_row: порядковый номер строки
            number_cell: порядковый номер ячейки
            check_text: ожидаемый тескст в ячейке
        """
        with allure.step(
            title=f'Проверка, что ячейки с номером {number_cell} '
            f'в строке под номером {number_row} имеет тескт {check_text}'
        ):
            expect(
                actual=self.cell_with_number_in_row(
                    number_row=number_row, number_cell=number_cell, **kwargs
                )
            ).to_have_text(expected=check_text)

    def click_cell_in_row_by_num(
        self, number_row: int, number_cell: int, **kwargs: str
    ) -> None:
        """Клик по ячейке с номером ячейки
        Args:
            number_row: порядковый номер строки
            number_cell: номер ячейки
        """
        with allure.step(
            title=f'Клик по ячейке с номером {number_cell} '
            f'в строке под номером {number_row}'
        ):
            self.cell_with_number_in_row(
                number_row=number_row, number_cell=number_cell, **kwargs
            ).click()

    def should_have_count_cell(
        self, count_cell: int, text_cell: str, **kwargs
    ) -> None:
        """Проверка, что количество записей в таблице равно указанному
        Args:
            count_cell: ожидаемое количество ячеек
            text_cell: текст искомых записей. Если None,
            возвращаем количество всех записей в таблице
        """
        with allure.step(
            title=f'Проверка, что количество записей '
            f'в таблице {self.name} равно {count_cell}'
        ):
            expect(
                actual=self.cell_by_text(text_cell=text_cell, **kwargs)
            ).to_have_count(count=count_cell)

    def column_header_by_text(self, text_column: str, **kwargs) -> Locator:
        """Колонка в таблице по тексту
        Args:
            text_column: текст колонки
            Return:
                Элемент типа Locator
        """
        row_header: Locator = self.row_header(**kwargs)
        return row_header.get_by_role(
            role='columnheader', name=text_column, exact=True
        )

    def __repr__(self):
        return self.locator