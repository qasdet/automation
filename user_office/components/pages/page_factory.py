"""
Фабрика для создания Page Objects в User Office.

Этот модуль реализует паттерн Factory Method для создания page objects.
Позволяет стандартизировать и централизовать создание страниц.

Основные возможности:
    - Единая точка создания всех page objects
    - Type-safe создание через enum
    - Автоматическая регистрация страниц

Использование:
    # В fixture:
    @pytest.fixture
    def campaign_page(chromium_page):
        return PageFactory.create(chromium_page, PageType.CAMPAIGN)

    # В тесте:
    page = PageFactory.create(page, PageType.CAMPAIGNS_LIST)

Структура PageType enum:
    AUTHORIZATION - Страница авторизации
    DIGITAL_HOME - Главная страница digital
    CAMPAIGN - Страница кампании
    CAMPAIGNS_LIST - Страница списка кампаний
    ... (и другие)

Как добавить новую страницу:
    1. Создать класс страницы (наследованный от BasePage)
    2. Добавить новый тип в PageType enum
    3. Добавить регистрацию в register_pages()

Пример:
    # 1. Создаем класс
    class MyNewPage(BasePage):
        def __init__(self, page):
            super().__init__(page)
            self.model = MyModel(page)

    # 2. Добавляем тип
    class PageType(Enum):
        ...
        MY_NEW_PAGE = auto()

    # 3. Регистрируем
    @PageFactory.register(PageType.MY_NEW_PAGE)
    class MyNewPage(BasePage):
        ...
"""

from enum import Enum, auto
from typing import TYPE_CHECKING, Type

if TYPE_CHECKING:
    from playwright.sync_api import Page
    from user_office.components.base_page import BasePage


class PageType(Enum):
    """
    Перечисление всех типов страниц User Office.

    Используется для type-safe создания page objects через PageFactory.
    Каждый тип соответствует одной странице приложения.

    Примеры:
        >>> PageType.CAMPAIGN
        <PageType.CAMPAIGN: 4>
        >>> PageType.CAMPAIGN.name
        'CAMPAIGN'
        >>> PageType.CAMPAIGN.value
        4
    """

    #: Страница авторизации
    AUTHORIZATION = auto()

    #: Главная страница digital
    DIGITAL_HOME = auto()

    #: Страница кампании (карточка)
    CAMPAIGN = auto()

    #: Страница списка кампаний
    CAMPAIGNS_LIST = auto()

    #: Страница создания кампании
    CREATE_CAMPAIGN = auto()

    #: Страница просмотра о кампании
    ABOUT_CAMPAIGN = auto()

    #: Страница медиаплана
    MEDIAPLAN = auto()

    #: Страница создания медиаплана
    CREATE_MEDIAPLAN = auto()

    #: Страница размещений
    PLACEMENT = auto()

    #: Страница шаблонов размещений
    PLACEMENT_TEMPLATE = auto()

    #: Страница отчетности
    REPORTING = auto()

    #: Страница справочников
    DICTIONARIES = auto()

    #: Страница проверки здоровья приложения
    HEALTH_CHECK = auto()

    #: Страница инструкций
    INSTRUCTIONS = auto()

    #: Страница списка пользователей
    USERS = auto()

    #: Страница карточки пользователя
    USER_CARD = auto()

    #: Страница профиля медиаплана
    MEDIA_PLAN_PROFILE = auto()

    #: Страница стратегических планов
    STRAT_PLANS = auto()

    #: Страница конкретного стратегического плана
    SPECIFIC_STRAT_PLAN = auto()

    #: Страница TV кампаний
    TV_CAMPAIGNS = auto()

    #: Страница создания TV кампании
    CREATE_TV_CAMPAIGN = auto()

    #: Страница деталей TV кампании
    DETAILS_TV_CAMPAIGN = auto()

    #: Страница карточки TV кампании
    TV_CAMPAIGN_CARD = auto()

    #: Страница карточки TV медиаплана
    TV_MPLAN_CARD = auto()


class PageFactory:
    """
    Фабрика для создания Page Objects User Office.

    Реализует паттерн Factory Method с централизованной регистрацией
    всех страниц приложения.

    Основные методы:
        - register(): Декоратор для регистрации страницы
        - create(): Создать page object по типу
        - get_registered_pages(): Получить список зарегистрированных страниц

    Использование:

        # Создание страницы (основной метод):
        >>> page = PageFactory.create(chromium_page, PageType.CAMPAIGN)
        >>> isinstance(page, CampaignPage)
        True

        # Регистрация новой страницы:
        >>> @PageFactory.register(PageType.MY_NEW_PAGE)
        ... class MyNewPage(BasePage):
        ...     pass

        # Получить список доступных страниц:
        >>> PageFactory.get_registered_pages()
        [<PageType.CAMPAIGN>, <PageType.CAMPAIGNS_LIST>, ...]

    Attributes:
        _registry: Приватный словарь для хранения зарегистрированных классов страниц.
                  Ключ - PageType enum, значение - класс страницы (наследник BasePage).
    """

    _registry: dict[PageType, Type['BasePage']] = {}

    @classmethod
    def register(cls, page_type: PageType):
        """
        Декоратор для регистрации класса страницы.

        Используется для связывания класса страницы с её типом в enum PageType.
        После регистрации страницу можно создавать через create().

        Args:
            page_type: Значение из enum PageType, например PageType.CAMPAIGN

        Returns:
            Декоратор, который принимает класс страницы и регистрирует его

        Example:
            # Регистрация страницы кампании:
            >>> @PageFactory.register(PageType.CAMPAIGN)
            ... class CampaignPage(BasePage):
            ...     pass

            # Теперь можно создать:
            >>> page = PageFactory.create(page, PageType.CAMPAIGN)

        Note:
            Этот метод является декоратором, но также можно использовать
            как обычную функцию:
            >>> PageFactory.register(PageType.CAMPAIGN)(CampaignPage)
        """
        def decorator(page_class: Type['BasePage']) -> Type['BasePage']:
            """
            Декоратор, который регистрирует класс в реестре.

            Args:
                page_class: Класс страницы (наследник BasePage)

            Returns:
                Тот же класс (для совместимости с декоратором)
            """
            cls._registry[page_type] = page_class
            return page_class
        return decorator

    @classmethod
    def create(cls, page: 'Page', page_type: PageType) -> 'BasePage':
        """
        Создать экземпляр page object по его типу.

        Это основной метод фабрики. Принимает Playwright Page и тип страницы,
        возвращает соответствующий page object.

        Args:
            page: Playwright Page объект для взаимодействия с браузером.
                 Обычно получается из fixture chromium_page.
            page_type: Тип страницы из enum PageType.
                      Определяет какой класс страницы будет создан.

        Returns:
            Экземпляр соответствующего класса страницы (наследник BasePage)

        Raises:
            ValueError: Если переданный page_type не зарегистрирован

        Example:
            >>> page = PageFactory.create(chromium_page, PageType.CAMPAIGN)
            >>> page.visit('https://example.com/campaign/123')

            # Получение списка доступных типов:
            >>> registered = cls.get_registered_pages()
            >>> print([t.name for t in registered])
            ['AUTHORIZATION', 'CAMPAIGN', 'CAMPAIGNS_LIST', ...]

        Note:
            Перед созданием страницы убедитесь что она зарегистрирована.
            Все страницы регистрируются автоматически при импорте модуля.
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
        """
        Получить список всех зарегистрированных типов страниц.

        Returns:
            Список значений PageType для всех зарегистрированных страниц

        Example:
            >>> pages = PageFactory.get_registered_pages()
            >>> for page_type in pages:
            ...     print(page_type.name)
            AUTHORIZATION
            CAMPAIGN
            CAMPAIGNS_LIST
            ...
        """
        return list(cls._registry.keys())


def register_pages():
    """
    Регистрация всех страниц User Office в PageFactory.

    Этот метод вызывается автоматически при импорте модуля.
    Каждая страница регистрируется с соответствующим типом из PageType enum.

    Регистрируемые страницы:
        - AuthorizationPage (AUTHORIZATION)
        - DigitalHomePage (DIGITAL_HOME)
        - CampaignPage (CAMPAIGN)
        - CampaignsListPage (CAMPAIGNS_LIST)
        - CreateCampaignPage (CREATE_CAMPAIGN)
        - AboutCampaignPage (ABOUT_CAMPAIGN)
        - MediaplanPage (MEDIAPLAN)
        - CreateMediaplanPage (CREATE_MEDIAPLAN)
        - PlacementPage (PLACEMENT)
        - PlacementTemplatePage (PLACEMENT_TEMPLATE)
        - ReportingPage (REPORTING)
        - DictionariesPage (DICTIONARIES)
        - HealthCheckPage (HEALTH_CHECK)
        - InstructionsPage (INSTRUCTIONS)
        - UsersPage (USERS)
        - UserCardPage (USER_CARD)
        - MediaPlanProfilePage (MEDIA_PLAN_PROFILE)
        - StratPlansPage (STRAT_PLANS)
        - SpecificStratPlanPage (SPECIFIC_STRAT_PLAN)
        - TVCampaignsPage (TV_CAMPAIGNS)
        - CreateTVCampaignPage (CREATE_TV_CAMPAIGN)
        - DetailsTVCampaignPage (DETAILS_TV_CAMPAIGN)
        - TVCampaignCardPage (TV_CAMPAIGN_CARD)
        - TVMplanCardPage (TV_MPLAN_CARD)

    Note:
        Этот метод вызывается автоматически при импорте модуля page_factory.
        Не нужно вызывать его вручную.
    """
    from user_office.components.pages.authorization.authorization_page import AuthorizationPage
    from user_office.components.pages.digital_page.digital_home_page import DigitalHomePage
    from user_office.components.pages.campaigns.campaign_page import CampaignPage
    from user_office.components.pages.campaigns.campaigns_list_page import CampaignsListPage
    from user_office.components.pages.campaigns.create_campaign_page import CreateCampaignPage
    from user_office.components.pages.campaigns.about_campaign_page import AboutCampaignPage
    from user_office.components.pages.mediaplan.mediaplan_page import MediaplanPage
    from user_office.components.pages.mediaplan.create_mediaplan_page import CreateMediaplanPage
    from user_office.components.pages.placement.placement_page import PlacementPage
    from user_office.components.pages.placement_template.placement_template_page import PlacementTemplatePage
    from user_office.components.pages.reporting.reporting_page import ReportingPage
    from user_office.components.pages.dictionaries.dictionaries_page import DictionariesPage
    from user_office.components.pages.health_check.health_check_page import HealthCheckPage
    from user_office.components.pages.instructions_for_publication.instruction_page import InstructionsPage
    from user_office.components.pages.users.users_page import UsersPage
    from user_office.components.pages.users.user_card_page import UserCardPage
    from user_office.components.pages.profile.mediaplan_profile_page import MediaPlanProfilePage
    from user_office.components.pages.strat_plan.strat_plans_page import StratPlansPage
    from user_office.components.pages.strat_plan.specific_strat_plan_page import SpecificStratPlanPage
    from user_office.components.pages.tv.tv_campanings.tv_campaigns_page import TVCampaignsPage
    from user_office.components.pages.tv.tv_campanings.create_tv_campaign_page import CreateTVCampaignPage
    from user_office.components.pages.tv.tv_campanings.details_tv_campaign_page import DetailsTVCampaignPage
    from user_office.components.pages.tv.tv_campanings.tv_campaign_card_page import TVCampaignCardPage
    from user_office.components.pages.tv.tv_mplan.tv_mplan_card_page import TVMplanCardPage

    PageFactory.register(PageType.AUTHORIZATION)(AuthorizationPage)
    PageFactory.register(PageType.DIGITAL_HOME)(DigitalHomePage)
    PageFactory.register(PageType.CAMPAIGN)(CampaignPage)
    PageFactory.register(PageType.CAMPAIGNS_LIST)(CampaignsListPage)
    PageFactory.register(PageType.CREATE_CAMPAIGN)(CreateCampaignPage)
    PageFactory.register(PageType.ABOUT_CAMPAIGN)(AboutCampaignPage)
    PageFactory.register(PageType.MEDIAPLAN)(MediaplanPage)
    PageFactory.register(PageType.CREATE_MEDIAPLAN)(CreateMediaplanPage)
    PageFactory.register(PageType.PLACEMENT)(PlacementPage)
    PageFactory.register(PageType.PLACEMENT_TEMPLATE)(PlacementTemplatePage)
    PageFactory.register(PageType.REPORTING)(ReportingPage)
    PageFactory.register(PageType.DICTIONARIES)(DictionariesPage)
    PageFactory.register(PageType.HEALTH_CHECK)(HealthCheckPage)
    PageFactory.register(PageType.INSTRUCTIONS)(InstructionsPage)
    PageFactory.register(PageType.USERS)(UsersPage)
    PageFactory.register(PageType.USER_CARD)(UserCardPage)
    PageFactory.register(PageType.MEDIA_PLAN_PROFILE)(MediaPlanProfilePage)
    PageFactory.register(PageType.STRAT_PLANS)(StratPlansPage)
    PageFactory.register(PageType.SPECIFIC_STRAT_PLAN)(SpecificStratPlanPage)
    PageFactory.register(PageType.TV_CAMPAIGNS)(TVCampaignsPage)
    PageFactory.register(PageType.CREATE_TV_CAMPAIGN)(CreateTVCampaignPage)
    PageFactory.register(PageType.DETAILS_TV_CAMPAIGN)(DetailsTVCampaignPage)
    PageFactory.register(PageType.TV_CAMPAIGN_CARD)(TVCampaignCardPage)
    PageFactory.register(PageType.TV_MPLAN_CARD)(TVMplanCardPage)


# Автоматическая регистрация всех страниц при импорте модуля
register_pages()
