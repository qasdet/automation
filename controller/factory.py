"""
Базовые компоненты UI для Playwright тестов.

Модуль содержит базовый класс Factory и набор mixin классов (примесей),
которые обеспечивают функциональность для работы с UI элементами.

Архитектура:
    Factory - базовый класс с обязательными свойствами (page, name, locator, type_of)
    Mixins  - необязательные модули функциональности (click, fill, assert и т.д.)

Использование:
    # Компонент со всеми возможностями:
    >>> class Button(ClickableMixin, AssertableMixin, Factory):
    ...     @property
    ...     def type_of(self) -> str:
    ...         return 'button'

    # Компонент только с кликом:
    >>> class SimpleButton(ClickableMixin, Factory):
    ...     pass

Список mixins:
    - ClickableMixin: click, hover, highlight
    - FillableMixin: fill, clear, append, should_be_empty
    - AssertableMixin: should_be_visible, should_have_text, etc.
    - GettableMixin: inner_text, text_content, input_value, is_visible
    - UtilityMixin: matching_by_text, file_check_in_folder

Базовый пример:
    >>> class MyComponent(ClickableMixin, AssertableMixin, Factory):
    ...     @property
    ...     def type_of(self) -> str:
    ...         return 'my_component'
    ...
    ...     def custom_action(self) -> 'MyComponent':
    ...         self.click()
    ...         return self
"""

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import TypeVar

import allure
from playwright.sync_api import Locator, Page, expect

this_dir = Path(__file__).resolve().parent

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filename=f'{this_dir}/pytest.log',
    filemode='w',
)

T = TypeVar('T', bound='Factory')


# =============================================================================
# BASE FACTORY CLASS
# =============================================================================

class Factory(ABC):
    """
    Базовый класс для всех UI компонентов.

    Определяет обязательные свойства и базовый функционал,
    который должен быть у любого компонента страницы.

    Attributes:
        page: Playwright Page объект для взаимодействия с браузером
        name: Название компонента для отображения в логах и allure отчетах
        locator: Базовый XPath/CSS локатор элемента (с поддержкой форматирования)
    """

    def __init__(self, page: Page, locator: str, name: str) -> None:
        """
        Инициализировать компонент.

        Args:
            page: Playwright Page объект для взаимодействия с браузером
            locator: XPath/CSS локатор элемента. Может содержать
                    placeholder-ы для format() например {contains_text}
            name: Название компонента для логирования и отчетности
        """
        self.page: Page = page
        self.name: str = name
        self.locator: str = locator

    @property
    @abstractmethod
    def type_of(self) -> str:
        """
        Тип компонента для отчетности в allure.

        Returns:
            str: Название типа компонента (button, input, link и т.д.)
        """
        return 'component'

    def get_locator(self, **kwargs) -> Locator:
        """
        Получить Playwright локатор с подстановкой параметров.

        Args:
            **kwargs: Параметры для форматирования локатора.
                    Например: contains_text="Кнопка", number_row=1

        Returns:
            Locator: Настроенный Playwright локатор

        Example:
            >>> component.get_locator(contains_text="Отправить", number_row=2)
        """
        locator: str = self.locator.format(**kwargs)
        logging.info(f'I see you: locator {locator}')
        return self.page.locator(locator)

    def _log_action(self, action: str) -> None:
        """Логирование действия с компонентом."""
        logging.info(f'{action} {self.type_of} with name "{self.name}"')

    def __repr__(self) -> str:
        """Строковое представление компонента."""
        return self.locator


# =============================================================================
# MIXIN CLASSES
# =============================================================================

class ClickableMixin:
    """Mixin для компонентов с возможностью клика и наведения."""

    def click(self, **kwargs) -> 'Factory':
        """Кликнуть по элементу."""
        with allure.step(f'Clicking {self.type_of} "{self.name}"'):
            self._log_action('Clicking')
            self.get_locator(**kwargs).click()
        return self

    def hover(self, **kwargs) -> 'Factory':
        """Навести курсор на элемент."""
        with allure.step(f'Hovering over {self.type_of} "{self.name}"'):
            self._log_action('Hovering')
            self.get_locator(**kwargs).hover()
        return self

    def highlight(self, **kwargs) -> 'Factory':
        """Подсветить элемент (для отладки)."""
        self.get_locator(**kwargs).highlight()
        return self


class FillableMixin:
    """Mixin для компонентов с возможностью заполнения текстом."""

    def fill(self, value: str, **kwargs) -> 'Factory':
        """Заполнить поле ввода указанным значением."""
        with allure.step(f'Filling {self.type_of} "{self.name}" with "{value}"'):
            self.get_locator(**kwargs).fill(value)
        return self

    def clear(self, **kwargs) -> 'Factory':
        """Очистить поле ввода (удалить весь текст)."""
        with allure.step(f'Clearing {self.type_of} "{self.name}"'):
            self.get_locator(**kwargs).fill('')
        return self

    def append(self, value: str, **kwargs) -> 'Factory':
        """Добавить текст к уже существующему значению поля."""
        with allure.step(f'Appending "{value}" to {self.type_of} "{self.name}"'):
            locator = self.get_locator(**kwargs)
            current = locator.input_value()
            locator.fill(current + value)
        return self

    def should_be_empty(self, **kwargs) -> 'Factory':
        """Проверить, что поле ввода пустое."""
        with allure.step(f'Checking {self.type_of} "{self.name}" is empty'):
            expect(self.get_locator(**kwargs)).to_have_value('')
        return self


class AssertableMixin:
    """Mixin для компонентов с assertions (проверками состояния)."""

    def should_be_visible(self, timeout: float = 10.0, **kwargs) -> 'Factory':
        """Проверить, что элемент видим на странице."""
        with allure.step(f'Checking that {self.type_of} "{self.name}" is visible'):
            self._log_action('Checking visibility of')
            expect(
                actual=self.get_locator(**kwargs),
                message=f'Не вижу {self.type_of} "{self.name}"'
            ).to_be_visible(timeout=timeout)
        return self

    def should_not_be_visible(self, **kwargs) -> 'Factory':
        """Проверить, что элемент НЕ видим на странице."""
        with allure.step(f'Checking that {self.type_of} "{self.name}" is NOT visible'):
            self._log_action('Checking invisibility of')
            expect(
                actual=self.get_locator(**kwargs),
                message=f'Ожидал что {self.type_of} "{self.name}" не будет виден'
            ).not_to_be_visible()
        return self

    def should_have_text(self, text: str, **kwargs) -> 'Factory':
        """Проверить, что элемент содержит точно указанный текст."""
        with allure.step(f'Checking that {self.type_of} "{self.name}" has text "{text}"'):
            self._log_action('Checking text of')
            expect(
                actual=self.get_locator(**kwargs),
                message=f'Текст {self.type_of} "{self.name}" не соответствует'
            ).to_have_text(expected=text)
        return self

    def should_contain_text(self, text: str, **kwargs) -> 'Factory':
        """Проверить, что текст элемента содержит указанную подстроку."""
        with allure.step(f'Checking that {self.type_of} "{self.name}" contains text "{text}"'):
            expect(
                actual=self.get_locator(**kwargs),
                message=f'Текст {self.type_of} "{self.name}" не содержит "{text}"'
            ).to_contain_text(expected=text)
        return self

    def should_have_value(self, value: str, **kwargs) -> 'Factory':
        """Проверить значение поля ввода."""
        with allure.step(f'Checking that {self.type_of} "{self.name}" has value "{value}"'):
            expect(
                actual=self.get_locator(**kwargs),
                message=f'Значение {self.type_of} "{self.name}" не соответствует'
            ).to_have_value(value)
        return self

    def should_have_count(self, count: int, **kwargs) -> 'Factory':
        """Проверить количество элементов."""
        with allure.step(f'Checking that {self.type_of} "{self.name}" has {count} items'):
            expect(
                actual=self.get_locator(**kwargs),
                message=f'Количество элементов {self.type_of} "{self.name}" не соответствует'
            ).to_have_count(count=count)
        return self

    def should_be_enabled(self, **kwargs) -> 'Factory':
        """Проверить, что элемент доступен (enabled)."""
        with allure.step(f'Checking that {self.type_of} "{self.name}" is enabled'):
            expect(
                actual=self.get_locator(**kwargs),
                message=f'{self.type_of} "{self.name}" не доступен'
            ).to_be_enabled()
        return self

    def should_be_disabled(self, **kwargs) -> 'Factory':
        """Проверить, что элемент недоступен (disabled)."""
        with allure.step(f'Checking that {self.type_of} "{self.name}" is disabled'):
            expect(
                actual=self.get_locator(**kwargs),
                message=f'{self.type_of} "{self.name}" доступен, хотя ожидался недоступным'
            ).to_be_disabled()
        return self


class GettableMixin:
    """Mixin для получения данных из элементов (getters)."""

    def inner_text(self, **kwargs) -> str:
        """Получить innerText элемента."""
        with allure.step(f'Getting inner text of {self.type_of} "{self.name}"'):
            return self.get_locator(**kwargs).inner_text()

    def text_content(self, **kwargs) -> str:
        """Получить textContent элемента."""
        return self.get_locator(**kwargs).text_content()

    def input_value(self, **kwargs) -> str:
        """Получить значение поля ввода."""
        return self.get_locator(**kwargs).input_value()

    def is_visible(self, **kwargs) -> bool:
        """
        Проверить видимость элемента (без assert).

        Returns:
            bool: True если элемент видим, False иначе
        """
        return self.get_locator(**kwargs).is_visible()


class UtilityMixin:
    """Mixin для служебных методов."""

    def matching_by_text(self, **kwargs) -> None:
        """Найти элемент по тексту на странице."""
        with allure.step(f'Matching by text {self.type_of} "{self.name}"'):
            locator = self.get_locator(**kwargs)
            self.page.locator(selector=f'internal:text=("{locator}")')

    @staticmethod
    def file_check_in_folder(folder: str, file_format: str, numbers: int) -> None:
        """
        Проверить наличие файлов в папке по формату.

        Args:
            folder: Название папки для проверки
            file_format: Расширение файла (например '.pdf', '.xlsx')
            numbers: Количество уровней для подъема от текущей директории
        """
        current_path = Path.cwd().parents[numbers] / folder
        for file in current_path.iterdir():
            if file.suffix == file_format and file.is_file():
                assert file.is_file(), 'Файл отсутствует'
                assert file.suffix == file_format, 'Расширение файла не соответствует'