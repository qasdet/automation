from dataclasses import dataclass
from enum import Enum, auto


class MenuCategory(Enum):
    """Категории пунктов меню"""
    MAIN = auto()
    DICTIONARIES = auto()
    PRODUCT_PARAMETERS = auto()
    SOURCE_PARAMETERS = auto()
    OTHER = auto()


@dataclass
class MenuItem:
    """Конфигурация пункта меню"""
    name: str
    testid: str
    category: MenuCategory
    has_hover: bool = False


class SidebarConfig:
    """Конфигурация навигационного меню.

    Для добавления нового пункта меню - добавить строку в ITEMS.
    """
    ITEMS = [
        # MAIN
        MenuItem('Главная', 'sidebar_home', MenuCategory.MAIN),
        MenuItem('Доступы', 'sidebar_accesses', MenuCategory.MAIN),
        MenuItem('Пользователи', 'sidebar_users', MenuCategory.MAIN),
        MenuItem('Организации', 'sidebar_organizations', MenuCategory.MAIN),
        MenuItem('Справочники', 'sidebar_dictionaries', MenuCategory.MAIN),

        # DICTIONARIES
        MenuItem('Бренды', 'sidebar_brands', MenuCategory.DICTIONARIES),
        MenuItem('Клиенты', 'sidebar_clients', MenuCategory.DICTIONARIES),
        MenuItem('Каналы', 'sidebar_channels', MenuCategory.DICTIONARIES),
        MenuItem('Статусы размещений', 'sidebar_placement_statuses', MenuCategory.DICTIONARIES),
        MenuItem('Ценовые категории', 'sidebar_product_price_category', MenuCategory.DICTIONARIES),
        MenuItem('Заявки', 'sidebar_user_candidates', MenuCategory.DICTIONARIES),

        # PRODUCT_PARAMETERS
        MenuItem('Продукты', 'sidebar_products', MenuCategory.PRODUCT_PARAMETERS),
        MenuItem('Категории продуктов', 'sidebar_product_categories', MenuCategory.PRODUCT_PARAMETERS, has_hover=True),
        MenuItem('Сезонность', 'sidebar_product_seasonalities', MenuCategory.PRODUCT_PARAMETERS, has_hover=True),
        MenuItem('География', 'sidebar_product_geographies', MenuCategory.PRODUCT_PARAMETERS, has_hover=True),
        MenuItem('Типы продуктов', 'sidebar_product_types', MenuCategory.PRODUCT_PARAMETERS),

        # SOURCE_PARAMETERS
        MenuItem('Площадки', 'sidebar_sources', MenuCategory.SOURCE_PARAMETERS),
        MenuItem('Инструменты', 'sidebar_instruments', MenuCategory.SOURCE_PARAMETERS),

        # OTHER
        MenuItem('Рекламные размеры', 'sidebar_ad_sizes', MenuCategory.OTHER),
        MenuItem('Рекламные форматы', 'sidebar_ad_formats', MenuCategory.OTHER),
        MenuItem('Типы закупок', 'sidebar_buy_types', MenuCategory.OTHER),
        MenuItem('Известность бренда', 'sidebar_brand_awarenesses', MenuCategory.OTHER),
        MenuItem('Метрики', 'sidebar_metrics', MenuCategory.OTHER),
        MenuItem('Статусы кампаний', 'sidebar_campaign_statuses', MenuCategory.OTHER),
        MenuItem('Цели', 'sidebar_goals', MenuCategory.OTHER),
        MenuItem('Продавцы', 'sidebar_sellers', MenuCategory.OTHER),
    ]

    @classmethod
    def get_item(cls, name: str) -> MenuItem | None:
        """Получить пункт меню по имени"""
        return next((item for item in cls.ITEMS if item.name == name), None)

    @classmethod
    def get_items_by_category(cls, category: MenuCategory) -> list[MenuItem]:
        """Получить все пункты меню категории"""
        return [item for item in cls.ITEMS if item.category == category]
