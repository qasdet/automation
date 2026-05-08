import allure
from playwright.sync_api import expect

from controller.factory import AssertableMixin, ClickableMixin, Factory


class Tabbar(ClickableMixin, AssertableMixin, Factory):
    """
    Компонент для работы с панелью вкладок (tab bar/tab strip).

    Наследует функциональность от ClickableMixin (click, hover)
    и AssertableMixin для проверки состояния вкладок.

    Использование:
        >>> tabs = Tabbar(page, locator="[role='tablist']", name="Основные вкладки")
        >>> tabs.select_tab_by_text("Настройки").should_be_active_tab_by_text("Настройки")

    Примеры:
        Выбор вкладки:
        >>> Tabbar(page, "//div[@class='tabs']", "Меню").select_tab_by_text("Профиль")

        Проверка активной вкладки:
        >>> tabs.should_be_active_tab_by_text("Настройки")
    """

    @property
    def type_of(self) -> str:
        """Возвращает наименование типа компонента для логирования в allure"""
        return 'tabbar'

    def select_tab_by_text(self, name_tab: str, **kwargs) -> 'Tabbar':
        """
        Выбрать вкладку по тексту (названию).

        Выполняет клик по вкладке с указанным текстом.
        Текст должен точно совпадать с отображаемым названием вкладки.

        Args:
            name_tab (str): Название вкладки для выбора
            **kwargs: Параметры для форматирования локатора

        Returns:
            Tabbar: Возвращает self для fluent interface (цепочки вызовов)

        Example:
            >>> tabbar.select_tab_by_text("Настройки")
            >>> tabbar.select_tab_by_text("Профиль")
        """
        with allure.step(f'Selecting tab "{name_tab}"'):
            self.get_locator(**kwargs).get_by_text(name_tab).click()
        return self

    def should_be_visible_tab_by_text(self, name_tab: str, **kwargs) -> 'Tabbar':
        """
        Проверить, что вкладка с указанным текстом видима.

        Args:
            name_tab (str): Название вкладки для проверки
            **kwargs: Параметры для форматирования локатора

        Returns:
            Tabbar: Возвращает self для fluent interface

        Example:
            >>> tabbar.should_be_visible_tab_by_text("Настройки")
        """
        with allure.step(f'Checking tab "{name_tab}" is visible'):
            expect(
                self.get_locator(**kwargs).get_by_text(name_tab)
            ).to_be_visible()
        return self

    def should_be_active_tab_by_text(self, name_tab: str, **kwargs) -> 'Tabbar':
        """
        Проверить, что вкладка с указанным текстом является активной.

        Активная вкладка обычно имеет отличающийся визуальный стиль
        (выделение, другой цвет фона и т.д.). Метод проверяет текст
        в элементе .css-lt7pxj a.

        Args:
            name_tab (str): Название вкладки которая должна быть активной
            **kwargs: Параметры для форматирования локатора

        Returns:
            Tabbar: Возвращает self для fluent interface

        Example:
            >>> tabbar.should_be_active_tab_by_text("Профиль")
        """
        with allure.step(f'Checking tab "{name_tab}" is active'):
            expect(
                self.get_locator(**kwargs).locator('.css-lt7pxj').locator('a')
            ).to_have_text(name_tab)
        return self
