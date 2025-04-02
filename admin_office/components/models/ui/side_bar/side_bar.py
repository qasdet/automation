from playwright.sync_api import Page
from controller.link import Link
from controller.navigation_menu import NavigationMenu


class SideBar:
    """Навигационное меню в админ офисе"""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.navigation_menu = NavigationMenu(
            page=self.page,
            locator="[data-testid='admin_office_navigation_menu']",
            name='Навигационное меню',
        )
        self.main_link = Link(
            page=self.page,
            locator="[data-testid='sidebar_home']",
            name='Главная',
        )
        self.accesses_link = Link(
            page=self.page,
            locator="[data-testid='sidebar_accesses']",
            name='Доступы',
        )
        self.users_link = Link(
            page=self.page,
            locator="[data-testid='sidebar_users']",
            name='Пользователи',
        )
        self.organizations_link = Link(
            page=self.page,
            locator="[data-testid='sidebar_organizations']",
            name='Организации',
        )
        self.dictionaries_link = Link(
            page=self.page,
            locator="[data-testid='sidebar_dictionaries']",
            name='Справочники',
        )
        self.product_parameters_link = Link(
            page=self.page,
            locator="[data-testid='sidebar_spoiler_products_category']",
            name='Параметры продуктов',
        )
        self.products_link = Link(
            page=self.page,
            locator="[data-testid='sidebar_products']",
            name='Продукты',
        )
        self.product_categories_link = Link(
            page=self.page,
            locator="[data-testid='sidebar_product_categories']",
            name='Категории продуктов',
        )
        self.product_seasonality_link = Link(
            page=self.page,
            locator="[data-testid='sidebar_product_seasonalities']",
            name='Сезонность продуктов',
        )
        self.product_seasonality_value_link = Link(
            page=self.page,
            locator="[data-testid='sidebar_product_seasonality_values']",
            name='Значения сезонности продуктов',
        )
        self.product_geography_link = Link(
            page=self.page,
            locator="[data-testid='sidebar_product_geographies']",
            name='География продукта',
        )
        self.product_price_category_link = Link(
            page=self.page,
            locator="[data-testid='sidebar_product_price_category']",
            name='Ценовые категории продукта',
        )
        self.product_purchases_frequencies_link = Link(
            page=self.page,
            locator="[data-testid='sidebar_product_purchases_frequencies']",
            name='Частота покупки продукта',
        )
        self.product_types_link = Link(
            page=self.page,
            locator="[data-testid='sidebar_product_types']",
            name='Типы продуктов',
        )
        self.sources_category_link = Link(
            page=self.page,
            locator="[data-testid='sidebar_spoiler_sources_category']",
            name='Параметры площадок',
        )
        self.sources_link = Link(
            page=self.page,
            locator="[data-testid='sidebar_sources']",
            name='Площадки',
        )
        self.instruments_link = Link(
            page=self.page,
            locator="[data-testid='sidebar_instruments']",
            name='Инструменты',
        )
        self.sellers_link = Link(
            page=self.page,
            locator="[data-testid='sidebar_sellers']",
            name='Продавцы',
        )
        self.ad_sizes_link = Link(
            page=self.page,
            locator="[data-testid='sidebar_ad_sizes']",
            name='Рекламные размеры',
        )
        self.ad_formats_link = Link(
            page=self.page,
            locator="[data-testid='sidebar_ad_formats']",
            name='Рекламные форматы',
        )
        self.buy_types_link = Link(
            page=self.page,
            locator="[data-testid='sidebar_buy_types']",
            name='Типы закупок',
        )
        self.brands_link = Link(
            page=self.page,
            locator="[data-testid='sidebar_brands']",
            name='Бренды',
        )
        self.user_candidates_link = Link(
            page=self.page,
            locator="[data-testid='sidebar_user_candidates']",
            name='Заявки',
        )
        self.brand_awareness_link = Link(
            page=self.page,
            locator="[data-testid='sidebar_brand_awarenesses']",
            name='Известность бренда',
        )
        self.channels_link = Link(
            page=self.page,
            locator="[data-testid='sidebar_channels']",
            name='Каналы',
        )
        self.clients_link = Link(
            page=self.page,
            locator="[data-testid='sidebar_clients']",
            name='Клиенты',
        )
        self.metrics_link = Link(
            page=self.page,
            locator="[data-testid='sidebar_metrics']",
            name='Метрики',
        )
        self.campaign_statuses_link = Link(
            page=self.page,
            locator="[data-testid='sidebar_campaign_statuses']",
            name='Статусы кампаний',
        )
        self.placement_statuses_link = Link(
            page=self.page,
            locator="[data-testid='sidebar_placement_statuses']",
            name='Статусы размещений',
        )
        self.goals_link = Link(
            page=self.page,
            locator="[data-testid='sidebar_goals']",
            name='Цели',
        )

    def goto(self, name_item: str):
        """Перейти к пункту"""
        self.navigation_menu.goto(name_item=name_item)

    def check_main_link(self):
        self.main_link.should_be_visible()
        self.main_link.click()

    def check_accesses_link(self):
        self.accesses_link.should_be_visible()
        self.accesses_link.click()

    def check_users_link(self):
        self.users_link.should_be_visible()
        self.users_link.click()

    def check_organizations_link(self):
        self.organizations_link.should_be_visible()
        self.organizations_link.click()

    def check_dictionaries_link(self):
        self.dictionaries_link.should_be_visible()
        self.dictionaries_link.click()

    def check_product_parameters_link(self):
        self.product_parameters_link.should_be_visible()
        self.product_parameters_link.click()

    def check_products_link(self):
        self.products_link.should_be_visible()
        self.products_link.click()

    def check_product_categories_link(self):
        self.product_categories_link.hover()
        self.product_categories_link.should_be_visible()
        self.product_categories_link.click()

    def check_product_seasonality_link(self):
        self.product_seasonality_link.hover()
        self.product_seasonality_link.should_be_visible()
        self.product_seasonality_link.click()

    def check_product_seasonality_value_link(self):
        self.product_seasonality_value_link.hover()
        self.product_seasonality_value_link.should_be_visible()
        self.product_seasonality_value_link.click()

    def check_product_geography_link(self):
        self.product_geography_link.hover()
        self.product_geography_link.should_be_visible()
        self.product_geography_link.click()

    def check_product_price_category_link(self):
        self.product_price_category_link.hover()
        self.product_price_category_link.should_be_visible()
        self.product_price_category_link.click()

    def check_product_purchases_frequencies_link(self):
        self.product_purchases_frequencies_link.hover()
        self.product_purchases_frequencies_link.should_be_visible()
        self.product_purchases_frequencies_link.click()

    def check_product_types_link(self):
        self.product_types_link.should_be_visible()
        self.product_types_link.click()

    def check_sources_category_link(self):
        self.sources_category_link.should_be_visible()
        self.sources_category_link.click()

    def check_sources_link(self):
        self.sources_link.should_be_visible()
        self.sources_link.click()

    def check_instruments_link(self):
        self.instruments_link.should_be_visible()
        self.instruments_link.click()

    def check_sellers_link(self):
        self.sellers_link.should_be_visible()
        self.sellers_link.click()

    def check_ad_sizes_link(self):
        self.ad_sizes_link.should_be_visible()
        self.ad_sizes_link.click()

    def check_ad_formats_link(self):
        self.ad_formats_link.should_be_visible()
        self.ad_formats_link.click()

    def check_buy_types_link(self):
        self.buy_types_link.should_be_visible()
        self.buy_types_link.click()

    def check_brands_link(self):
        self.brands_link.should_be_visible()
        self.brands_link.click()

    def check_user_candidates_link(self):
        self.user_candidates_link.should_be_visible()
        self.user_candidates_link.click()

    def check_brand_awareness_link(self):
        self.brand_awareness_link.should_be_visible()
        self.brand_awareness_link.click()

    def check_channels_link(self):
        self.channels_link.should_be_visible()
        self.channels_link.click()

    def check_clients_link(self):
        self.clients_link.should_be_visible()
        self.clients_link.click()

    def check_metrics_link(self):
        self.metrics_link.should_be_visible()
        self.metrics_link.click()

    def check_campaign_statuses_link(self):
        self.campaign_statuses_link.should_be_visible()
        self.campaign_statuses_link.click()

    def check_placement_statuses_link(self):
        self.placement_statuses_link.should_be_visible()
        self.placement_statuses_link.click()

    def check_goals_link(self):
        self.goals_link.should_be_visible()
        self.goals_link.click()

    def check_all_text(self):
        self.check_main_link()
        self.check_accesses_link()
        self.check_users_link()
        self.check_organizations_link()
        self.check_dictionaries_link()
        self.check_product_parameters_link()
        self.check_products_link()
        self.check_product_categories_link()
        self.check_product_seasonality_link()
        self.check_product_seasonality_value_link()
        self.check_product_geography_link()
        self.check_product_price_category_link()
        self.check_product_purchases_frequencies_link()
        self.check_product_types_link()
        self.check_sources_category_link()
        self.check_sources_link()
        self.check_instruments_link()
        self.check_sellers_link()
        self.check_ad_sizes_link()
        self.check_ad_formats_link()
        self.check_buy_types_link()
        self.check_brands_link()
        self.check_user_candidates_link()
        self.check_brand_awareness_link()
        self.check_channels_link()
        self.check_clients_link()
        self.check_metrics_link()
        self.check_campaign_statuses_link()
        self.check_placement_statuses_link()
        self.check_goals_link()
        self.check_product_parameters_link()
        self.check_sources_category_link()
