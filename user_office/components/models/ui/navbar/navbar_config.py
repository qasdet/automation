"""
Конфигурация навигационного меню User Office.

Этот модуль содержит данные о структуре навигационного меню:
- Пункты меню (название, локатор, категория)
- Категории пунктов меню

Использование:
    from user_office.components.models.ui.navbar import NavbarConfig, NavbarItem

    # Получить пункт меню по имени
    item = NavbarConfig.get_item('Кампании')

    # Получить все пункты категории
    items = NavbarConfig.get_items_by_category(NavbarCategory.DICTIONARIES)

Зачем это нужно:
    - Данные отделены от логики
    - Легко добавить новый пункт меню (1 строка)
    - Нет дублирования в коде

Пример добавления нового пункта меню:
    Добавить одну строку в ITEMS:
    >>> NavbarItem('Новый пункт', "//a[.='Новый']", NavbarCategory.OTHER),
"""

from dataclasses import dataclass
from enum import Enum, auto


class NavbarCategory(Enum):
    """
    Категории пунктов навигационного меню.

    Используется для группировки пунктов меню по назначению.
    Позволяет фильтровать пункты по категории.

    Values:
        MAIN: Главные разделы (Кампании, Справочники)
        CAMPAIGNS: Разделы, связанные с кампаниями
        DICTIONARIES: Справочники и словари
        OTHER: Прочие разделы (О сервисе, Поддержка)
    """
    MAIN = auto()
    CAMPAIGNS = auto()
    DICTIONARIES = auto()
    OTHER = auto()


@dataclass
class NavbarItem:
    """
    Конфигурация одного пункта навигационного меню.

    Представляет собой структуру данных для одного пункта меню:
    - Отображаемое имя (текст ссылки)
    - XPath локатор для поиска элемента
    - Категория (для группировки)
    - Флаг необходимости hover (для submenu)

    Attributes:
        name: Текст, отображаемый пользователю в меню.
              Должен точно соответствовать тексту элемента на странице.
        locator: XPath или CSS локатор для поиска элемента.
                 Используется Playwright для поиска и взаимодействия.
        category: Категория пункта меню из enum NavbarCategory.
                  Используется для группировки и фильтрации.
        has_hover: Флаг, указывающий нужен ли hover перед кликом.
                   True для пунктов с dropdown/submenu.

    Example:
        >>> item = NavbarItem(
        ...     name='Кампании',
        ...     locator="//a[.='Кампании']",
        ...     category=NavbarCategory.CAMPAIGNS,
        ...     has_hover=False
        ... )
    """
    name: str
    locator: str
    category: NavbarCategory
    has_hover: bool = False


class NavbarConfig:
    """
    Конфигурация навигационного меню User Office.

    Содержит статический список ITEMS с конфигурацией всех пунктов меню.
    Также предоставляет методы для поиска пунктов меню.

    Зачем нужен этот класс:
        1. Централизованное хранение данных о меню
        2. Один источник истины для локаторов
        3. Легкое добавление новых пунктов

    Attributes:
        ITEMS: Список всех пунктов меню (list of NavbarItem)

    Methods:
        get_item(name): Получить пункт меню по имени
        get_items_by_category(category): Получить все пункты категории

    Example:
        Получить локатор для пункта "Кампании":
        >>> item = NavbarConfig.get_item('Кампании')
        >>> print(item.locator)
        "//a[.='Кампании']"

    Как добавить новый пункт меню:
        Просто добавьте строку в список ITEMS:
        >>> ITEMS = [
        ...     NavbarItem('Кампании', "//a[.='Кампании']", NavbarCategory.CAMPAIGNS),
        ...     NavbarItem('Справочники', "//a[.='Справочники']", NavbarCategory.DICTIONARIES),
        ...     NavbarItem('Новый пункт', "//a[.='Новый']", NavbarCategory.OTHER),  # <-- Новая строка
        ... ]
    """

    ITEMS = [
        NavbarItem('Кампании', "//a[.='Кампании']", NavbarCategory.CAMPAIGNS),
        NavbarItem('Справочники', "//a[.='Справочники']", NavbarCategory.DICTIONARIES),
        NavbarItem('О сервисе', "//a[.='О сервисе']", NavbarCategory.OTHER),
        NavbarItem('Поддержка', "//a[.='Поддержка']", NavbarCategory.OTHER),
    ]

    @classmethod
    def get_item(cls, name: str) -> NavbarItem | None:
        """
        Получить пункт меню по имени.

        Args:
            name: Имя пункта меню (точно как отображается в интерфейсе)

        Returns:
            NavbarItem или None если пункт не найден

        Example:
            >>> item = NavbarConfig.get_item('Кампании')
            >>> if item:
            ...     print(f"Локатор: {item.locator}")
        """
        return next((item for item in cls.ITEMS if item.name == name), None)

    @classmethod
    def get_items_by_category(cls, category: NavbarCategory) -> list[NavbarItem]:
        """
        Получить все пункты меню указанной категории.

        Args:
            category: Категория из enum NavbarCategory

        Returns:
            Список NavbarItem принадлежащих категории

        Example:
            >>> dictionaries = NavbarConfig.get_items_by_category(NavbarCategory.DICTIONARIES)
            >>> for item in dictionaries:
            ...     print(item.name)
        """
        return [item for item in cls.ITEMS if item.category == category]
