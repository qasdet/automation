from playwright.sync_api import Page
from admin_office.components.base_page import BasePage
from admin_office.components.models.ui.product_price_categories.product_price_categories import (
    ProductPriceCategoriesUI,
)


class AdminOfficeProductPriceCategoriesPage(BasePage):
    """Статусы размещений"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.product_price_categories = ProductPriceCategoriesUI(page)

    def go_to_product_price_categories(self):
        """Перейти на страницу Ценовые категории продуктов"""
        self.side_bar.check_product_parameters_link()
        self.side_bar.check_product_price_category_link()
        self.product_price_categories.check_page_loading()
