import allure
from playwright.sync_api import Locator

from controller.factory import AssertableMixin, ClickableMixin, Factory


class DropDownList(ClickableMixin, AssertableMixin, Factory):
    """
    Компонент для работы с выпадающими списками (dropdown).

    Наследует функциональность от ClickableMixin (click, hover)
    и AssertableMixin для проверки состояния.

    Использование:
        >>> dropdown = DropDownList(page, locator="[data-testid='country-select']", name="Страна")
        >>> dropdown.select_item_by_text("Россия").should_have_selected_item("Россия")

    Примеры:
        Открытие и выбор элемента:
        >>> dropdown.open().select_item_by_text("Россия")

        Проверка выбранного элемента:
        >>> dropdown.should_have_selected_item("Германия")
    """

    @property
    def type_of(self) -> str:
        """Возвращает наименование типа компонента для логирования в allure"""
        return 'DropDownList'

    def field_input(self, **kwargs) -> Locator:
        """
        Получить локатор поля ввода внутри выпадающего списка.

        Возвращает input элемент внутри компонента, исключая скрытые типы.

        Args:
            **kwargs: Параметры для форматирования локатора

        Returns:
            Locator: Playwright локатор видимого input поля

        Example:
            >>> dropdown.field_input().input_value()
        """
        locator = self.get_locator(**kwargs)
        return locator.locator("input:not([type='hidden'])")

    def select_item_by_text(self, name_item: str, **kwargs) -> 'DropDownList':
        """
        Выбрать элемент из выпадающего списка по тексту.

        Открывает список кликом, находит элемент по точному совпадению
        текста и выполняет клик по нему. Закрывает список кликом
        в сторону (смещение 2px вверх).

        Args:
            name_item (str): Точный текст элемента для выбора
            **kwargs: Параметры для форматирования локатора

        Returns:
            DropDownList: Возвращает self для fluent interface

        Example:
            >>> dropdown.select_item_by_text("Россия")
            >>> dropdown.select_item_by_text("Германия")
        """
        with allure.step(f'Selecting item "{name_item}" in {self.type_of} "{self.name}"'):
            self.click(**kwargs)
            locator = self.get_locator(**kwargs)
            locator.get_by_text(name_item, exact=True).click()
            self.page.mouse.click(x=2, y=0)
        return self

    def open(self, **kwargs) -> 'DropDownList':
        """
        Открыть выпадающий список.

        Выполняет клик по компоненту для раскрытия списка опций.

        Args:
            **kwargs: Параметры для форматирования локатора

        Returns:
            DropDownList: Возвращает self для fluent interface

        Example:
            >>> dropdown.open()
        """
        with allure.step(f'Opening {self.type_of} "{self.name}"'):
            self.click(**kwargs)
        return self

    def close(self, **kwargs) -> 'DropDownList':
        """
        Закрыть выпадающий список кликом в сторону.

        Выполняет клик в точку (2, 0) относительно страницы,
        что обычно закрывает выпадающий список без выбора элемента.

        Args:
            **kwargs: Параметры для форматирования локатора

        Returns:
            DropDownList: Возвращает self для fluent interface

        Example:
            >>> dropdown.close()
        """
        self.page.mouse.click(x=2, y=0)
        return self

    def should_have_selected_item(self, name_item: str, **kwargs) -> 'DropDownList':
        """
        Проверить, что в списке выбран указанный элемент.

        Args:
            name_item (str): Текст элемента, который должен быть выбран
            **kwargs: Параметры для форматирования локатора

        Returns:
            DropDownList: Возвращает self для fluent interface

        Example:
            >>> dropdown.should_have_selected_item("Россия")
        """
        with allure.step(f'Checking that "{name_item}" is selected in {self.type_of} "{self.name}"'):
            self.should_have_text(name_item, **kwargs)
        return self

    def get_selected_text(self, **kwargs) -> str:
        """
        Получить текст выбранного элемента.

        Возвращает текущее значение поля ввода внутри компонента,
        которое соответствует выбранному элементу.

        Args:
            **kwargs: Параметры для форматирования локатора

        Returns:
            str: Текст выбранного элемента

        Example:
            >>> selected = dropdown.get_selected_text()
            >>> print(f"Выбрано: {selected}")
        """
        return self.field_input(**kwargs).input_value()

    def is_item_visible(self, name_item: str, **kwargs) -> bool:
        """
        Проверить видимость элемента в раскрытом списке (без assert).

        Открывает список, ищет опцию по тексту и проверяет её видимость.
        Не выполняет assert, возвращает просто boolean.

        Args:
            name_item (str): Текст элемента для проверки
            **kwargs: Параметры для форматирования локатора

        Returns:
            bool: True если элемент с текстом виден в списке, False иначе

        Example:
            >>> if dropdown.is_item_visible("Россия"):
            ...     print("Россия доступна в списке")
        """
        with allure.step(f'Checking item "{name_item}" visibility in {self.type_of} "{self.name}"'):
            self.open(**kwargs)
            return self.page.get_by_role("option", name=name_item).is_visible()

    def __repr__(self) -> str:
        """Строковое представление объекта (локатор)"""
        return self.locator