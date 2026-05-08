import allure
from playwright.sync_api import Page

from controller.button import Button
from controller.factory import AssertableMixin, ClickableMixin, Factory


class Paging(ClickableMixin, AssertableMixin, Factory):
    """
    Компонент для работы с элементами пагинации.

    Наследует функциональность от ClickableMixin (click, hover)
    и AssertableMixin для проверки состояния.

    Использование:
        >>> paging = Paging(page, locator="[data-testid='pagination']", name="Пагинация")
        >>> paging.go_to_page(3).go_to_next_page()

    Примеры:
        Переход на следующую страницу:
        >>> paging.go_to_next_page()

        Переход к конкретной странице:
        >>> paging.go_to_page(5)
    """

    @property
    def type_of(self) -> str:
        """Возвращает наименование типа компонента для логирования в allure"""
        return 'Paging'

    def __init__(self, page: Page, locator: str, name: str) -> None:
        """
        Инициализировать компонент пагинации.

        Args:
            page: Playwright Page объект для взаимодействия с браузером
            locator (str): Базовый XPath/CSS локатор компонента пагинации
            name (str): Название компонента для отображения в логах

        Note:
            Автоматически создает дочерние Button объекты для кнопок
            "Предыдущая" и "Следующая" страница.
        """
        super().__init__(page, locator, name)
        self.prev_button = Button(
            self.page,
            locator=f'{locator}//button[1]',
            name='Предыдущая страница',
        )
        self.next_button = Button(
            self.page,
            locator=f'{locator}//button[2]',
            name='Следующая страница',
        )

    def go_to_next_page(self) -> 'Paging':
        """
        Перейти на следующую страницу.

        Проверяет видимость кнопки "Следующая" и выполняет клик.

        Returns:
            Paging: Возвращает self для fluent interface (цепочки вызовов)

        Example:
            >>> paging.go_to_next_page()
        """
        self.next_button.should_be_visible().click()
        return self

    def go_to_prev_page(self) -> 'Paging':
        """
        Перейти на предыдущую страницу.

        Проверяет видимость кнопки "Предыдущая" и выполняет клик.

        Returns:
            Paging: Возвращает self для fluent interface

        Example:
            >>> paging.go_to_prev_page()
        """
        self.prev_button.should_be_visible().click()
        return self

    def go_to_page(self, page_number: int) -> 'Paging':
        """
        Перейти к конкретной странице по номеру.

        Выполняет клик по кнопке с указанным номером страницы.

        Args:
            page_number (int): Номер страницы для перехода (начиная с 1)

        Returns:
            Paging: Возвращает self для fluent interface

        Example:
            >>> paging.go_to_page(3)  # Переход к странице 3
            >>> paging.go_to_page(10)  # Переход к странице 10
        """
        with allure.step(f'Going to page {page_number}'):
            self.page.get_by_role('button', name=str(page_number)).click()
        return self
