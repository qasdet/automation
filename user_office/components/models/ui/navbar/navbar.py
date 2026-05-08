"""
Фасад для навигационного меню User Office.

Этот модуль реализует паттерн Facade для работы с навигационным меню.
Предоставляет простой интерфейс для навигации по приложению.

Основные возможности:
    - Единый метод navigate_to() для всех пунктов меню
    - Lazy loading для ProfileModal
    - Обратная совместимость через deprecated методы

Использование:
    # Новый способ (рекомендуется):
    navbar.navigate_to('Кампании')
    navbar.navigate_to('Справочники')

    # Старый способ (deprecated, но работает):
    navbar.visit_campaigns()
    navbar.visit_references()

Структура:
    navbar.py         - Фасад с логикой навигации
    navbar_config.py - Данные (названия, локаторы, категории)

Пример добавления нового пункта меню:
    1. Открыть navbar_config.py
    2. Добавить строку в NavbarConfig.ITEMS:
       NavbarItem('Новый', "//a[.='Новый']", NavbarCategory.OTHER)
    3. Готово - navigate_to('Новый') будет работать автоматически
"""

import warnings
from typing import TYPE_CHECKING

import allure
from controller.link import Link

from user_office.components.models.ui.navbar.navbar_config import (
    NavbarCategory,
    NavbarItem,
    NavbarConfig,
)

if TYPE_CHECKING:
    from playwright.sync_api import Page
    from user_office.components.models.ui.profile_modal.profile_modal import ProfileModal


class Navbar:
    """
    Фасад для работы с навигационным меню User Office.

    Этот класс инкапсулирует логику работы с навигационным меню и предоставляет
    простой интерфейс для навигации по разделам приложения.

    Основной метод:
        - navigate_to(item_name): Переход к любому пункту меню

    Дополнительные методы:
        - profile_open(): Открыть профиль пользователя
        - profile_user(): Перейти к информации о пользователе

    Attributes:
        page: Playwright Page объект для взаимодействия с браузером
        _links: Кэш созданных Link объектов (для оптимизации)

    Использование:
        >>> navbar = Navbar(page)
        >>> navbar.navigate_to('Кампании')  # Перейти к кампаниям
        >>> navbar.navigate_to('Справочники')  # Перейти к справочникам

        # Fluent interface (методы возвращают self):
        >>> navbar.navigate_to('Кампании').navigate_to('Справочники')
    """

    def __init__(self, page: 'Page') -> None:
        """
        Инициализировать Navbar.

        Args:
            page: Playwright Page объект для взаимодействия с браузером.
                  Обычно получается из fixture chromium_page.
        """
        self.page = page
        self._links: dict[str, Link] = {}

    def _init_links(self) -> dict[str, Link]:
        """
        Инициализировать (создать) все Link объекты для пунктов меню.

        Создает словарь Link объектов, где ключ - это имя пункта меню,
        а значение - объект Link для взаимодействия с этим пунктом.

        Returns:
            dict[str, Link]: Словарь {имя_пункта: Link_объект}

        Note:
            Этот метод вызывается автоматически при первом обращении к _links.
            Используется lazy initialization - объекты создаются только когда нужны.
        """
        return {
            item.name: Link(
                page=self.page,
                locator=item.locator,
                name=item.name,
            )
            for item in NavbarConfig.ITEMS
        }

    def navigate_to(self, item_name: str) -> 'Navbar':
        """
        Перейти к указанному пункту меню.

        Это основной метод для навигации. Принимает имя пункта меню,
        находит соответствующий Link объект и выполняет клик.

        Args:
            item_name: Название пункта меню точно как оно отображается
                      в интерфейсе. Например: 'Кампании', 'Справочники'.

        Returns:
            Navbar: Возвращает self для fluent interface (цепочки вызовов)

        Raises:
            ValueError: Если пункт меню не найден среди зарегистрированных

        Example:
            >>> navbar.navigate_to('Кампании')  # Клик по ссылке "Кампании"
            >>> navbar.navigate_to('Справочники')  # Клик по ссылке "Справочники"

            # Fluent interface:
            >>> navbar.navigate_to('Кампании').navigate_to('Справочники')

        Note:
            Если для пункта меню установлен флаг has_hover=True,
            перед кликом будет выполнен hover.
        """
        # Lazy initialization для ссылок
        if not self._links:
            self._links = self._init_links()

        link = self._links.get(item_name)
        if not link:
            available = ', '.join(self._links.keys())
            raise ValueError(
                f"Navbar item '{item_name}' not found. Available: {available}"
            )

        menu_item = NavbarConfig.get_item(item_name)
        if not menu_item:
            raise ValueError(f"Navbar config not found for '{item_name}'")

        with allure.step(f'Navigate to "{item_name}"'):
            if menu_item.has_hover:
                link.hover()
            link.click()

        return self

    # === PROFILE METHODS ===
    # Эти методы относятся к профилю пользователя, а не к основной навигации

    @property
    def profile_modal(self) -> 'ProfileModal':
        """
        Получить объект ProfileModal для работы с модальным окном профиля.

        Использует lazy loading - объект создается только при первом обращении.

        Returns:
            ProfileModal: Объект для работы с модальным окном профиля

        Example:
            >>> navbar.profile_modal.modal_open()  # Открыть профиль
            >>> navbar.profile_modal.profile_user_modal()  # Перейти к информации о пользователе
        """
        from user_office.components.models.ui.profile_modal.profile_modal import ProfileModal
        return ProfileModal(self.page)

    def profile_open(self) -> 'Navbar':
        """
        Открыть модальное окно профиля пользователя.

        Returns:
            Navbar: Возвращает self для fluent interface

        Example:
            >>> navbar.profile_open()  # Открывает модальное окно профиля
        """
        self.profile_modal.modal_open()
        return self

    def profile_user(self) -> 'Navbar':
        """
        Перейти к информации о пользователе в модальном окне профиля.

        Открывает модальное окно профиля и переходит к вкладке/секции
        "Профиль пользователя".

        Returns:
            Navbar: Возвращает self для fluent interface

        Example:
            >>> navbar.profile_user()  # Открывает профиль и переходит к информации о пользователе
        """
        self.profile_modal.profile_user_modal()
        return self

    # === DEPRECATED: методы для обратной совместимости ===
    # Эти методы сохранены для совместимости со старым кодом.
    # Рекомендуется использовать navigate_to() вместо них.

    def visit_campaigns(self) -> None:
        """
        Перейти к разделу Кампании.

        .. deprecated::
            Используйте :meth:`navigate_to` вместо этого метода:

            >>> navbar.navigate_to('Кампании')

        Warning:
            Этот метод устарел и будет удален в будущих версиях.
        """
        warnings.warn(
            "Use navigate_to('Кампании') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('Кампании')

    def visit_references(self) -> None:
        """
        Перейти к разделу Справочники.

        .. deprecated::
            Используйте :meth:`navigate_to` вместо этого метода:

            >>> navbar.navigate_to('Справочники')

        Warning:
            Этот метод устарел и будет удален в будущих версиях.
        """
        warnings.warn(
            "Use navigate_to('Справочники') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('Справочники')

    def visit_about_services(self) -> None:
        """
        Перейти к разделу О сервисе.

        .. deprecated::
            Используйте :meth:`navigate_to` вместо этого метода:

            >>> navbar.navigate_to('О сервисе')

        Warning:
            Этот метод устарел и будет удален в будущих версиях.
        """
        warnings.warn(
            "Use navigate_to('О сервисе') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('О сервисе')

    def visit_support(self) -> None:
        """
        Перейти к разделу Поддержка.

        .. deprecated::
            Используйте :meth:`navigate_to` вместо этого метода:

            >>> navbar.navigate_to('Поддержка')

        Warning:
            Этот метод устарел и будет удален в будущих версиях.
        """
        warnings.warn(
            "Use navigate_to('Поддержка') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('Поддержка')
