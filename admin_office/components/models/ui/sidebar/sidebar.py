import warnings
from typing import TYPE_CHECKING

import allure
from controller.link import Link
from controller.navigation_menu import NavigationMenu

from admin_office.components.models.ui.sidebar.sidebar_config import (
    MenuCategory,
    MenuItem,
    SidebarConfig,
)

if TYPE_CHECKING:
    from playwright.sync_api import Page


class SideBar:
    """Фасад для навигационного меню.

    Использование:
        side_bar.navigate_to('Бренды')
        side_bar.navigate_to('Клиенты', category=MenuCategory.DICTIONARIES)
    """

    def __init__(self, page: 'Page') -> None:
        self.page = page
        self._navigation_menu = NavigationMenu(
            page=page,
            locator="[data-testid='admin_office_navigation_menu']",
            name='Навигационное меню',
        )
        self._links = self._init_links()

    def _init_links(self) -> dict[str, Link]:
        """Ленивая инициализация ссылок меню"""
        return {
            item.name: Link(
                page=self.page,
                locator=f"[data-testid='{item.testid}']",
                name=item.name,
            )
            for item in SidebarConfig.ITEMS
        }

    def navigate_to(
        self,
        item_name: str,
        category: MenuCategory | None = None,
    ) -> 'SideBar':
        """Перейти к указанному пункту меню.

        Args:
            item_name: Название пункта меню
            category: Категория (опционально, для disambiguation)
        """
        link = self._links.get(item_name)
        if not link:
            available = ', '.join(self._links.keys())
            raise ValueError(
                f"Menu item '{item_name}' not found. Available: {available}"
            )

        menu_item = SidebarConfig.get_item(item_name)
        if not menu_item:
            raise ValueError(f"Menu item config not found for '{item_name}'")

        with allure.step(f'Navigate to "{item_name}"'):
            if menu_item.has_hover:
                link.hover()
            link.click()

        return self

    @property
    def navigation_menu(self) -> NavigationMenu:
        """Доступ к навигационному меню"""
        return self._navigation_menu

    # === DEPRECATED: методы для обратной совместимости ===

    def check_brands_link(self) -> None:
        """@deprecated Use navigate_to('Бренды')"""
        warnings.warn(
            "Use navigate_to('Бренды') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('Бренды')

    def check_users_link(self) -> None:
        """@deprecated Use navigate_to('Пользователи')"""
        warnings.warn(
            "Use navigate_to('Пользователи') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('Пользователи')

    def check_organizations_link(self) -> None:
        """@deprecated Use navigate_to('Организации')"""
        warnings.warn(
            "Use navigate_to('Организации') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('Организации')

    def check_clients_link(self) -> None:
        """@deprecated Use navigate_to('Клиенты')"""
        warnings.warn(
            "Use navigate_to('Клиенты') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('Клиенты')

    def check_channels_link(self) -> None:
        """@deprecated Use navigate_to('Каналы')"""
        warnings.warn(
            "Use navigate_to('Каналы') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('Каналы')

    def check_products_link(self) -> None:
        """@deprecated Use navigate_to('Продукты')"""
        warnings.warn(
            "Use navigate_to('Продукты') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('Продукты')

    def check_sources_link(self) -> None:
        """@deprecated Use navigate_to('Площадки')"""
        warnings.warn(
            "Use navigate_to('Площадки') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('Площадки')

    def check_instruments_link(self) -> None:
        """@deprecated Use navigate_to('Инструменты')"""
        warnings.warn(
            "Use navigate_to('Инструменты') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('Инструменты')

    def check_main_link(self) -> None:
        """@deprecated Use navigate_to('Главная')"""
        warnings.warn(
            "Use navigate_to('Главная') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('Главная')

    def check_accesses_link(self) -> None:
        """@deprecated Use navigate_to('Доступы')"""
        warnings.warn(
            "Use navigate_to('Доступы') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('Доступы')

    def check_dictionaries_link(self) -> None:
        """@deprecated Use navigate_to('Справочники')"""
        warnings.warn(
            "Use navigate_to('Справочники') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('Справочники')

    def check_placement_statuses_link(self) -> None:
        """@deprecated Use navigate_to('Статусы размещений')"""
        warnings.warn(
            "Use navigate_to('Статусы размещений') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('Статусы размещений')

    def check_product_price_category_link(self) -> None:
        """@deprecated Use navigate_to('Ценовые категории')"""
        warnings.warn(
            "Use navigate_to('Ценовые категории') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('Ценовые категории')

    def check_user_candidates_link(self) -> None:
        """@deprecated Use navigate_to('Заявки')"""
        warnings.warn(
            "Use navigate_to('Заявки') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('Заявки')

    def check_product_categories_link(self) -> None:
        """@deprecated Use navigate_to('Категории продуктов')"""
        warnings.warn(
            "Use navigate_to('Категории продуктов') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('Категории продуктов')

    def check_product_seasonality_link(self) -> None:
        """@deprecated Use navigate_to('Сезонность')"""
        warnings.warn(
            "Use navigate_to('Сезонность') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('Сезонность')

    def check_product_seasonality_value_link(self) -> None:
        """@deprecated Use navigate_to('Значения сезонности')"""
        warnings.warn(
            "Use navigate_to('Значения сезонности') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('Значения сезонности')

    def check_product_geography_link(self) -> None:
        """@deprecated Use navigate_to('География')"""
        warnings.warn(
            "Use navigate_to('География') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('География')

    def check_product_purchases_frequencies_link(self) -> None:
        """@deprecated Use navigate_to('Частота покупки')"""
        warnings.warn(
            "Use navigate_to('Частота покупки') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('Частота покупки')

    def check_product_types_link(self) -> None:
        """@deprecated Use navigate_to('Типы продуктов')"""
        warnings.warn(
            "Use navigate_to('Типы продуктов') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('Типы продуктов')

    def check_sources_category_link(self) -> None:
        """@deprecated Use navigate_to('Параметры площадок')"""
        warnings.warn(
            "Use navigate_to('Параметры площадок') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('Параметры площадок')

    def check_sellers_link(self) -> None:
        """@deprecated Use navigate_to('Продавцы')"""
        warnings.warn(
            "Use navigate_to('Продавцы') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('Продавцы')

    def check_ad_sizes_link(self) -> None:
        """@deprecated Use navigate_to('Рекламные размеры')"""
        warnings.warn(
            "Use navigate_to('Рекламные размеры') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('Рекламные размеры')

    def check_ad_formats_link(self) -> None:
        """@deprecated Use navigate_to('Рекламные форматы')"""
        warnings.warn(
            "Use navigate_to('Рекламные форматы') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('Рекламные форматы')

    def check_buy_types_link(self) -> None:
        """@deprecated Use navigate_to('Типы закупок')"""
        warnings.warn(
            "Use navigate_to('Типы закупок') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('Типы закупок')

    def check_brand_awareness_link(self) -> None:
        """@deprecated Use navigate_to('Известность бренда')"""
        warnings.warn(
            "Use navigate_to('Известность бренда') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('Известность бренда')

    def check_metrics_link(self) -> None:
        """@deprecated Use navigate_to('Метрики')"""
        warnings.warn(
            "Use navigate_to('Метрики') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('Метрики')

    def check_campaign_statuses_link(self) -> None:
        """@deprecated Use navigate_to('Статусы кампаний')"""
        warnings.warn(
            "Use navigate_to('Статусы кампаний') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('Статусы кампаний')

    def check_goals_link(self) -> None:
        """@deprecated Use navigate_to('Цели')"""
        warnings.warn(
            "Use navigate_to('Цели') instead",
            DeprecationWarning,
            stacklevel=2,
        )
        self.navigate_to('Цели')
