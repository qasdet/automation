import allure
from playwright.sync_api import Locator, expect

from controller.factory import Factory


class Table(Factory):
    def type_of(self) -> str:
        return 'table'

    def tbody(self, **kwargs) -> Locator:
        """Тело таблицы"""
        return self.get_locator(**kwargs).locator(selector_or_locator='tbody')

    def cell_by_text(self, text_cell: str, **kwargs) -> Locator:
        """Ячейка в таблице по тексту (не привязана к строке)
        Args:
            text_cell: текст ячейки
        Return:
            Элемент типа Locator
        """
        tbody: Locator = self.tbody(**kwargs)
        return tbody.get_by_role(role='cell', name=text_cell, exact=True)

    def cell_in_head(self, text_cell: str, **kwargs) -> Locator:
        """Ячейка в шапке таблицы по тексту
        Args:
            text_cell: текст ячейки
        Return:
            Элемент типа Locator
        """

        table: Locator = self.get_locator(**kwargs)
        return table.locator(selector_or_locator='thead').get_by_role(
            role='cell', name=text_cell
        )

    def row_with_number(self, number_row: int, **kwargs) -> Locator:
        """Строка таблицы по порядковому номеру
        Args:
            number_row: порядковый номер строки
        Return:
            Элемент типа Locator
        """

        tbody: Locator = self.tbody(**kwargs)
        return tbody.get_by_role(role='row').nth(index=number_row)

    def row_by_contains_text(self, text_row: str, **kwargs) -> Locator:
        """Строка таблицы включает текст
        Args:
            text_row: текст строки
        Return:
            Элемент типа Locator
        """

        tbody: Locator = self.tbody(**kwargs)
        return tbody.get_by_role(role='row', name=text_row)

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
        ).get_by_role(role='cell', name=text_cell, exact=True)

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
            .get_by_role(role='cell')
            .nth(index=number_cell)
        )

    def cell_with_text_in_row_by_contains_text(
        self, text_row: str, text_cell: str, **kwargs
    ) -> Locator:
        """Ячейка c текстом в строке по указанному тексту
        Args:
            text_row: текст строки
            text_cell: текст ячейки
        Return:
            Элемент типа Locator
        """

        return self.row_by_contains_text(
            text_row=text_row, **kwargs
        ).get_by_role(role='cell', name=text_cell, exact=True)

    def cell_with_number_in_row_by_contains_text(
        self, text_row: str, number_cell: int, **kwargs
    ) -> Locator:
        """Ячейка по порядковому номеру в строке
        Args:
            text_row: текст строки
            number_cell: порядковый номер ячейки
        Return:
            Элемент типа Locator
        """
        return (
            self.row_by_contains_text(text_row=text_row, **kwargs)
            .get_by_role(role='cell')
            .nth(index=number_cell)
        )

    def button_menu_action_in_row(self, number_row: int, **kwargs) -> Locator:
        """Кнопка меню действий в строке
        Args:
            number_row: порядковый номер строки
        Return:
            Элемент типа Locator
        """
        return self.row_with_number(number_row=number_row, **kwargs).locator(
            selector_or_locator='button'
        )

    def button_menu_action_in_row_by_contains_text(
        self, text_row: str, **kwargs
    ) -> Locator:
        """Кнопка меню действий в строке
        Args:
            text_row: текст строки
        Return:
            Элемент типа Locator
        """
        return self.row_by_contains_text(text_row=text_row, **kwargs).locator(
            selector_or_locator='button'
        )

    def menu_action_in_table(self) -> Locator:
        """Контекстное меню действий над записью"""
        return self.page.locator("[role='dialog']")

    # Методы для взаимодействия с таблицей
    def should_be_visible_cell_by_text(self, text_cell: str, **kwargs) -> None:
        """Проверка, что ячейка с текстом  отображается (не привязана к строке)
        Args:
            text_cell: текст ячейки
        """
        expect(
            actual=self.cell_by_text(text_cell=text_cell, **kwargs)
        ).to_be_visible()

    def should_be_visible_row_by_contains_text(
        self, text_row: str, **kwargs
    ) -> None:
        """Проверка, что строка с текстом  отображается)
        Args:
            text_row: текст ячейки
        """
        expect(
            actual=self.row_by_contains_text(text_row=text_row, **kwargs)
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

    def should_be_visible_cell_in_row_by_contains_text(
        self, text_row: str, text_cell: str, **kwargs
    ) -> None:
        """Проверка, что ячейка с текстом в указанной строке отображается
        Args:
            text_row: текст строки
            text_cell: текст ячейки
        """
        with allure.step(
            title=f'Проверка, что ячейки с текстом {text_cell} '
            f'в строке {text_row} отображается'
        ):
            expect(
                actual=self.cell_with_text_in_row_by_contains_text(
                    text_row=text_row, text_cell=text_cell, **kwargs
                )
            ).to_be_visible()

    def should_have_text_cell_in_row_by_contains_text(
        self, text_row: str, number_cell, check_text: str, **kwargs
    ) -> None:
        """Проверка, что ячейка с порядковым номером
        в указанной строке отображается
        Args:
            text_row: порядковый номер строки
            number_cell: порядковый номер ячейки
            check_text: ожидаемый текст в ячейке
        """
        with allure.step(
            title=f'Проверка, что ячейки с номером {number_cell} '
            f'в строке {text_row} имеет текст {check_text}'
        ):
            expect(
                actual=self.cell_with_number_in_row_by_contains_text(
                    text_row=text_row, number_cell=number_cell, **kwargs
                )
            ).to_have_text(expected=check_text)

    def click_cell_in_row(
        self, number_row: int, text_cell: str, **kwargs: str
    ) -> None:
        """Клик по ячейке в указанной строке
        Args:
            number_row: порядковый номер строки
            text_cell: текст ячейки
        """
        with allure.step(
            title=f'Клик по ячейке с текстом {text_cell} '
            f'в строке под номером {number_row}'
        ):
            self.cell_with_text_in_row(
                number_row=number_row, text_cell=text_cell, **kwargs
            ).click()

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

    # Действия с меню действий
    def open_menu_action_in_row(self, number_row: int, **kwargs) -> None:
        """Открыть меню действий в указанной строке
        Args:
            number_row: порядковый номер строки
        """
        with allure.step(
            title=f'Открыть меню действий в строке под номером {number_row}'
        ):
            self.button_menu_action_in_row(
                number_row=number_row, **kwargs
            ).click()
            self.should_be_visible_button_menu_action_in_row(
                number_row=number_row, **kwargs
            )

    def open_menu_action_in_row_by_contains_text(
        self, text_row: str, **kwargs
    ) -> None:
        """Открыть меню действий в указанной строке
        Args:
            text_row: текст строки
        """
        with allure.step(
            title=f'Открыть меню действий в строке в строке {text_row}'
        ):
            self.button_menu_action_in_row_by_contains_text(
                text_row=text_row, **kwargs
            ).click()
            self.should_be_visible_button_menu_action_in_row_by_contains_text(
                text_row=text_row, **kwargs
            )

    def click_item_menu_action(self, text_item: str) -> None:
        """Клик по действию в меню действий над строкой
        Args:
            text_item: действие над записью
        """
        with allure.step(
            title=f'Клик по действию {text_item} '
            f'в меню действий в таблице {self.name}'
        ):
            self.menu_action_in_table().get_by_text(
                text=text_item, exact=True
            ).click()

    def should_be_visible_button_menu_action_in_row(
        self, number_row: int, **kwargs
    ) -> None:
        """Проверка, что кнопка меню действий в указанной строке отображается
        Args:
            number_row: порядковый номер строки
        """
        with allure.step(
            title=f'Проверка, что кнопка меню действий '
            f'в строке под номером {number_row} отображается'
        ):
            expect(
                actual=self.button_menu_action_in_row(
                    number_row=number_row, **kwargs
                )
            ).to_be_visible()

    def should_be_visible_button_menu_action_in_row_by_contains_text(
        self, text_row: str, **kwargs
    ) -> None:
        """Проверка, что кнопка меню действий в указанной строке отображается
        Args:
            text_row: текст строки
        """
        with allure.step(
            title=f'Проверка, что кнопка меню действий '
            f'в строке {text_row} отображается'
        ):
            expect(
                actual=self.button_menu_action_in_row_by_contains_text(
                    text_row=text_row, **kwargs
                )
            ).to_be_visible()

    def should_be_visible_menu_action_in_table(self) -> None:
        """Проверка, что меню действий отображается"""
        with allure.step(
            title=f'Проверка, что меню действий отображается в таблице {self.name}'
        ):
            expect(actual=self.menu_action_in_table()).to_be_visible()

    # Действия с таблицей
    def should_have_count_row(
        self, count_row: int, text_row: str = None, **kwargs
    ) -> None:
        """Проверка, что количество записей в таблице равно указанному
        Args:
            count_row: ожидаемое количество записей
            text_row: текст искомых записей. Если None,
            возвращаем количество всех записей в таблице
        """
        with allure.step(
            title=f'Проверка, что количество записей '
            f'в таблице {self.name} равно {count_row}'
        ):
            tbody: Locator = self.tbody(**kwargs)
            expect(
                actual=tbody.get_by_role(role='row', name=text_row)
            ).to_have_count(count=count_row)

    def count_rows(self, text_row: str = None) -> int:
        """Количество записей в таблице
        Args:
            text_row: текст искомых записей. Если None,
            возвращаем количество всех записей в таблице
        Return:
            Количество строк
        """
        return (
            self.get_locator()
            .locator(selector_or_locator='tbody')
            .get_by_role(role='row', name=text_row)
            .count()
        )

    def __repr__(self):
        return self.locator