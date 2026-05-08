import allure

from controller.factory import AssertableMixin, ClickableMixin, Factory


class NavigationMenu(ClickableMixin, AssertableMixin, Factory):
    """
    Компонент для работы с навигационным меню.

    Наследует функциональность от ClickableMixin (click, hover)
    и AssertableMixin для проверки состояния.

    Использование:
        >>> menu = NavigationMenu(page, locator="nav.main-menu", name="Главное меню")
        >>> menu.goto("Настройки").click()

    Примеры:
        Переход к пункту меню:
        >>> NavigationMenu(page, "//nav[@class='sidebar']", "Боковое меню").goto("Профиль")

        Проверка видимости меню:
        >>> menu.should_be_visible()
    """

    @property
    def type_of(self) -> str:
        """Возвращает наименование типа компонента для логирования в allure"""
        return 'navigation menu'

    def goto(self, name_item: str) -> 'NavigationMenu':
        """
        Перейти к указанному пункту меню.

        Выполняет проверку видимости пункта меню, затем клик по нему.
        Является основным методом навигации.

        Args:
            name_item (str): Название пункта меню для перехода.
                           Должно точно соответствовать тексту элемента.

        Returns:
            NavigationMenu: Возвращает self для fluent interface (цепочки вызовов)

        Example:
            >>> menu = NavigationMenu(page, "nav.sidebar", "Боковое меню")
            >>> menu.goto("Настройки")  # Клик по пункту "Настройки"
            >>> menu.goto("Профиль").should_be_visible()  # Fluent interface
        """
        with allure.step(f'Navigating to menu item "{name_item}"'):
            self.should_be_visible(item_name=name_item)
            self.click(item_name=name_item)
        return self
