"""
Базовый класс для всех Page Objects в User Office.

Этот модуль является точкой входа для всех страниц приложения User Office.
Каждая страница наследуется от BasePage и получает общий функционал.

Использование:
    class CampaignPage(BasePage):
        def __init__(self, page: Page) -> None:
            super().__init__(page)
            self.campaign_model = CampaignModel(page)

Основные возможности:
    - Управление Playwright Page через self.page
    - Lazy loading для компонентов (navbar)
    - Методы навигации (visit, reload)
    - Проверка текущей страницы (should_be_on_page)

Примеры:
    >>> page = CampaignPage(browser_page)
    >>> page.visit("https://example.com/campaigns")
    >>> page.navbar.navigate_to('Кампании')
    >>> page.should_be_on_page('/campaigns')
"""

import allure
import httpx
from playwright.sync_api import Page, Response
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

# Отключаем предупреждения о небезопасных HTTPS соединениях
disable_warnings(InsecureRequestWarning)


class BasePage:
    """
    Базовый класс для всех страниц User Office.

    Этот класс предоставляет общий функционал для всех page objects:
    - Доступ к Playwright Page
    - Lazy loading компонентов (Navbar)
    - Методы навигации
    - Проверка текущей страницы

    Attributes:
        page (Page): Playwright Page объект для взаимодействия с браузером

    Usage:
        Не используйте этот класс напрямую. Наследуйтесь от него:

        >>> class MyPage(BasePage):
        ...     def __init__(self, page: Page):
        ...         super().__init__(page)
        ...         self.my_component = MyComponent(page)
    """

    def __init__(self, page: Page) -> None:
        """
        Инициализировать BasePage.

        Args:
            page: Playwright Page объект, представляющий текущую страницу браузера.
                  Создается через browser.new_page() или chromium_page fixture.
        """
        self.page: Page = page

    @property
    def navbar(self):
        """
        Получить объект навигационного меню (Navbar).

        Используется lazy loading - объект создается только при первом обращении.
        Это экономит память и время если тест не использует меню.

        Returns:
            Navbar: Объект для работы с навигационным меню

        Example:
            >>> base_page = BasePage(page)
            >>> base_page.navbar.navigate_to('Кампании')

        Note:
            Не вызывает self.page.wait_for_url() или других действий,
            только создает объект Navbar при первом обращении.
        """
        from user_office.components.models.ui.navbar import Navbar
        return Navbar(self.page)

    @property
    def url(self) -> str:
        """
        Получить текущий URL страницы.

        Returns:
            str: Текущий URL страницы, включая protocol, host, path и query.

        Example:
            >>> page.url
            'https://example.com/campaigns?tab=digital'
        """
        return self.page.url

    def visit(self, url: str) -> Response:
        """
        Перейти по указанному URL.

        Использует httpx для выполнения GET запроса (чтобы получить редирект),
        затем открывает финальный URL в браузере через Playwright.

        Args:
            url: Полный URL для перехода (например, 'https://example.com/campaigns')

        Returns:
            Response: Объект ответа Playwright от финальной страницы

        Example:
            >>> page.visit("https://example.com/campaigns")
            # Сначала делает GET запрос для обработки редиректа
            # Затем открывает финальный URL в браузере

        Note:
            Если URL содержит redirect, метод корректно обработает их
            и откроет финальную страницу после редиректа.
        """
        with allure.step(f'Opening URL: {url}'):
            with httpx.Client(http2=True, verify=False) as client:
                response = client.get(url=url)
            return self.page.goto(url=str(response.url), wait_until='domcontentloaded')

    def reload(self) -> Response:
        """
        Перезагрузить текущую страницу.

        Returns:
            Response: Объект ответа Playwright от перезагруженной страницы

        Example:
            >>> page.reload()
        """
        with allure.step(f'Reloading page: {self.url}'):
            return self.page.reload(wait_until='domcontentloaded')

    def should_be_on_page(self, url_fragment: str) -> bool:
        """
        Проверить, что текущий URL содержит указанную подстроку.

        Используется для проверки, что пользователь находится на правильной странице
        после навигации или действия.

        Args:
            url_fragment: Подстрока, которая должна присутствовать в URL.
                         Может быть:
                         - Часть пути ('/campaigns')
                         - Полный URL ('https://example.com/campaigns')
                         - Query параметр ('tab=digital')

        Returns:
            bool: True если подстрока найдена в URL, False иначе

        Example:
            >>> page.should_be_on_page('/campaigns')
            True
            >>> page.should_be_on_page('tab=digital')
            True
            >>> page.should_be_on_page('/users')
            False
        """
        return url_fragment in self.page.url
