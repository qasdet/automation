from playwright.sync_api import Page

from admin_office.components.base_page import BasePage
from admin_office.components.models.ui.products.product_card import ProductCard
from admin_office.components.models.ui.products.products import Products


class AdminOfficeProductsPage(BasePage):
    """Продукты"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.products = Products(page)
        self.product_card = ProductCard(page)

    def go_to_products(self) -> None:
        """Перейти в справочник Продукты"""
        self.side_bar.check_product_parameters_link()
        self.side_bar.check_products_link()
        self.products.check_page_loading()
