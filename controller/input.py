import allure
from playwright.sync_api import expect

from controller.factory import AssertableMixin, ClickableMixin, FillableMixin, Factory


class Input(ClickableMixin, FillableMixin, AssertableMixin, Factory):
    """
    Компонент для работы с текстовыми полями ввода.

    Наследует функциональность от:
    - ClickableMixin: click, hover (наследуется от Factory)
    - FillableMixin: fill, clear, append, should_be_empty
    - AssertableMixin: should_be_visible, should_have_value, etc.

    Использование:
        >>> input_field = Input(page, locator="[data-testid='username']", name="Имя пользователя")
        >>> input_field.fill("ivanov").should_have_value("ivanov")

    Примеры:
        Заполнение и проверка значения:
        >>> Input(page, "input[name='email']", "Email").fill("test@example.com")

        Очистка поля:
        >>> input_field.clear().fill("new_value")

        Добавление текста к существующему:
        >>> input_field.append(" + suffix")
    """

    @property
    def type_of(self) -> str:
        """Возвращает наименование типа компонента для логирования в allure"""
        return 'input'

    def fill(
        self, value: str, validate_value: bool = False, **kwargs
    ) -> 'Input':
        """
        Заполнить поле ввода указанным значением.

        Очищает текущее значение поля и вводит новое.
        Опционально можно проверить, что значение было установлено корректно.

        Args:
            value (str): Значение для ввода в поле
            validate_value (bool): Если True, выполнить проверку что
                                 значение поля равно введенному значению
            **kwargs: Параметры для форматирования локатора

        Returns:
            Input: Возвращает self для fluent interface (цепочки вызовов)

        Example:
            >>> input_field.fill("ivanov")  # Просто заполнить
            >>> input_field.fill("ivanov", validate_value=True)  # Заполнить и проверить
        """
        with allure.step(f'Filling {self.type_of} "{self.name}" with "{value}"'):
            locator = self.get_locator(**kwargs)
            locator.fill(value)
            if validate_value:
                expect(locator).to_have_value(value)
        return self

    def fill_by_label(
        self, label_value: str, value_to_fill: str, **kwargs
    ) -> 'Input':
        """
        Заполнить поле ввода по названию связанного label.

        Выполняет поиск input элемента по тексту его label и заполняет его.
        Использует page.get_by_label() для поиска.

        Args:
            label_value (str): Текст label элемента
            value_to_fill (str): Значение для ввода
            **kwargs: Параметры для форматирования локатора

        Returns:
            Input: Возвращает self для fluent interface

        Example:
            >>> input_field.fill_by_label("Email", "test@example.com")
        """
        with allure.step(f'Filling {self.type_of} "{self.name}" by label'):
            locator = self.get_locator(**kwargs)
            locator.page.get_by_label(label_value).fill(value_to_fill)
        return self

    def clear(self, **kwargs) -> 'Input':
        """
        Очистить поле ввода (удалить весь текст).

        Заполняет поле пустой строкой, что приводит к очистке содержимого.

        Args:
            **kwargs: Параметры для форматирования локатора

        Returns:
            Input: Возвращает self для fluent interface

        Example:
            >>> input_field.clear()
        """
        with allure.step(f'Clearing {self.type_of} "{self.name}"'):
            self.get_locator(**kwargs).fill('')
        return self

    def append(self, value: str, **kwargs) -> 'Input':
        """
        Добавить текст к уже существующему значению поля.

        Сначала получает текущее значение поля, затем добавляет
        к нему указанный текст.

        Args:
            value (str): Текст для добавления к текущему значению
            **kwargs: Параметры для форматирования локатора

        Returns:
            Input: Возвращает self для fluent interface

        Example:
            >>> input_field.fill("Hello").append(" World")
            # Результат: "Hello World"
        """
        with allure.step(f'Appending "{value}" to {self.type_of} "{self.name}"'):
            locator = self.get_locator(**kwargs)
            current = locator.input_value()
            locator.fill(current + value)
        return self

    def should_be_empty(self, **kwargs) -> 'Input':
        """
        Проверить, что поле ввода пустое.

        Использует expect для проверки значения поля на пустую строку.

        Args:
            **kwargs: Параметры для форматирования локатора

        Returns:
            Input: Возвращает self для fluent interface

        Example:
            >>> input_field.should_be_empty()
        """
        with allure.step(f'Checking {self.type_of} "{self.name}" is empty'):
            expect(self.get_locator(**kwargs)).to_have_value('')
        return self
