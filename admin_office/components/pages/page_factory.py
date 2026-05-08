from enum import Enum, auto
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from playwright.sync_api import Page
    from admin_office.components.base_page import BasePage


class PageType(Enum):
    """Типы страниц Admin Office"""
    HOME = auto()
    AUTHORIZATION = auto()
    BRANDS = auto()
    ORGANIZATIONS = auto()
    CHANNELS = auto()
    CLIENTS = auto()
    PRODUCTS = auto()
    SOURCES = auto()
    INSTRUMENTS = auto()
    USERS = auto()
    PLACEMENT_STATUSES = auto()
    PRODUCT_PRICE_CATEGORIES = auto()
    USER_CANDIDATES = auto()
    LANDING = auto()


class PageFactory:
    """Фабрика для создания Page Objects.

    Использование:
        page = PageFactory.create(page, PageType.BRANDS)
    """

    _registry: dict[PageType, Type['BasePage']] = {}

    @classmethod
    def register(cls, page_type: PageType):
        """Декоратор для регистрации страницы.

        Использование:
            @PageFactory.register(PageType.BRANDS)
            class AdminOfficeBrandsPage(BasePage):
                ...
        """
        def decorator(page_class: Type['BasePage']) -> Type['BasePage']:
            cls._registry[page_type] = page_class
            return page_class
        return decorator

    @classmethod
    def create(cls, page: 'Page', page_type: PageType) -> 'BasePage':
        """Создать Page Object по типу страницы.

        Args:
            page: Playwright Page
            page_type: Тип страницы из enum PageType

        Returns:
            Экземпляр соответствующего Page Object

        Raises:
            ValueError: Если страница не зарегистрирована
        """
        if page_type not in cls._registry:
            registered = [pt.name for pt in cls._registry.keys()]
            raise ValueError(
                f"Page type {page_type.name} not registered. "
                f"Registered pages: {registered}"
            )
        return cls._registry[page_type](page)

    @classmethod
    def get_registered_pages(cls) -> list[PageType]:
        """Получить список зарегистрированных типов страниц."""
        return list(cls._registry.keys())


def register_pages():
    """Регистрация всех страниц.

    Вызывается автоматически при импорте модуля.
    """
    from admin_office.components.pages.home.home_page import AdminOfficeHomePage
    from admin_office.components.pages.authorization.authorization_page import AdminOfficeAuthorizationPage
    from admin_office.components.pages.brands.brands_page import AdminOfficeBrandsPage
    from admin_office.components.pages.organizations.organizations_page import AdminOfficeOrganizationsPage
    from admin_office.components.pages.channels.channels_page import AdminOfficeChannelsPage
    from admin_office.components.pages.clients.clients_page import AdminOfficeClientsPage
    from admin_office.components.pages.products.products_page import AdminOfficeProductsPage
    from admin_office.components.pages.sources.sources_page import AdminOfficeSourcesPage
    from admin_office.components.pages.instruments.instruments_page import AdminOfficeInstrumentsPage
    from admin_office.components.pages.users.users_page import AdminOfficeUsersPage
    from admin_office.components.pages.placement_statuses.placement_statuses_page import AdminOfficePlacementStatusesPage
    from admin_office.components.pages.product_price_categories.product_price_categories_page import AdminOfficeProductPriceCategoriesPage
    from admin_office.components.pages.user_candidates.user_candidates_page import AdminOfficeUserCandidatesPage
    from admin_office.components.pages.landing.landing_page import LandingPage

    PageFactory.register(PageType.HOME)(AdminOfficeHomePage)
    PageFactory.register(PageType.AUTHORIZATION)(AdminOfficeAuthorizationPage)
    PageFactory.register(PageType.BRANDS)(AdminOfficeBrandsPage)
    PageFactory.register(PageType.ORGANIZATIONS)(AdminOfficeOrganizationsPage)
    PageFactory.register(PageType.CHANNELS)(AdminOfficeChannelsPage)
    PageFactory.register(PageType.CLIENTS)(AdminOfficeClientsPage)
    PageFactory.register(PageType.PRODUCTS)(AdminOfficeProductsPage)
    PageFactory.register(PageType.SOURCES)(AdminOfficeSourcesPage)
    PageFactory.register(PageType.INSTRUMENTS)(AdminOfficeInstrumentsPage)
    PageFactory.register(PageType.USERS)(AdminOfficeUsersPage)
    PageFactory.register(PageType.PLACEMENT_STATUSES)(AdminOfficePlacementStatusesPage)
    PageFactory.register(PageType.PRODUCT_PRICE_CATEGORIES)(AdminOfficeProductPriceCategoriesPage)
    PageFactory.register(PageType.USER_CANDIDATES)(AdminOfficeUserCandidatesPage)
    PageFactory.register(PageType.LANDING)(LandingPage)


# Автоматическая регистрация при импорте
register_pages()
