import allure
import requests
from playwright.sync_api import Page, Response

from admin_office.components.models.ui.sidebar import SideBar


class BasePage:
    """
    Базовый класс для всех страниц Admin Office.

    Этот класс предоставляет общий функционал для всех page objects
    в разделе Admin Office:
    - Доступ к Playwright Page
    - Lazy loading компонентов (SideBar)
    - Методы навигации (visit, reload)
    - Проверка текущей страницы (should_be_on_page)

    Использование:
        Не используйте этот класс напрямую. Наследуйтесь от него:

        >>> class AdminOfficeBrandsPage(BasePage):
        ...     def __init__(self, page: Page) -> None:
        ...         super().__init__(page)
        ...         self.brands = Brands(page)
        ...         self.card_brand = BrandCard(page)

    Attributes:
        page (Page): Playwright Page объект для взаимодействия с браузером
    """

    def __init__(self, page: Page) -> None:
        """
        Инициализировать BasePage.

        Args:
            page: Playwright Page объект, представляющий текущую страницу браузера.
                  Создается через browser.new_page() или chromium_page fixture.
        """
        self.page = page

    @property
    def side_bar(self) -> SideBar:
        """
        Получить объект боковой панели (SideBar).

        Использует lazy loading - объект создается только при первом обращении.
        Это экономит память и время если тест не использует боковую панель.

        Returns:
            SideBar: Объект для работы с боковой панелью навигации

        Example:
            >>> base_page = AdminOfficeBasePage(page)
            >>> base_page.side_bar.navigate_to("Бренды")
        """
        return SideBar(self.page)

    @property
    def url(self) -> str:
        """
        Получить текущий URL страницы.

        Returns:
            str: Текущий URL страницы, включая protocol, host, path и query

        Example:
            >>> page.url
            'https://admin.example.com/dictionaries/brands'
        """
        return self.page.url

    def visit(self, url: str) -> Response:
        """
        Перейти по указанному URL через requests для получения редиректа.

        Использует библиотеку requests для выполнения GET запроса (чтобы
        корректно обработать редиректы), затем открывает финальный URL
        в браузере через Playwright.

        Args:
            url: Полный URL для перехода
                 (например, 'https://admin.example.com/dictionaries/brands')

        Returns:
            Response: Объект ответа Playwright от финальной страницы

        Example:
            >>> page.visit("https://admin.example.com/dictionaries/brands")
        """
        with allure.step(f'Opening URL: {url}'):
            response = requests.get(url, verify=False)
            return self.page.goto(response.url)

    def reload(self) -> Response:
        """
        Перезагрузить текущую страницу.

        Использует wait_until='domcontentloaded' для ожидания полной загрузки DOM
        перед возвратом управления.

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

        Используется для проверки, что пользователь находится на правильной
        странице после навигации или действия.

        Args:
            url_fragment: Подстрока, которая должна присутствовать в URL.
                         Может быть:
                         - Часть пути ('/brands')
                         - Полный URL ('https://example.com/brands')
                         - Query параметр ('tab=digital')

        Returns:
            bool: True если подстрока найдена в URL, False иначе

        Example:
            >>> page.should_be_on_page('/brands')
            True
            >>> page.should_be_on_page('dictionaries')
            True
        """
        return url_fragment in self.page.url
