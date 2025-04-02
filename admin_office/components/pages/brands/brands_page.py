from playwright.sync_api import Page

from admin_office.components.base_page import BasePage
from admin_office.components.models.ui.brands.brand_card import BrandCard
from admin_office.components.models.ui.brands.brands import Brands


class AdminOfficeBrandsPage(BasePage):
    """Бренды"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.brands = Brands(page)
        self.card_brand = BrandCard(page)

    def go_to_brands(self) -> None:
        """Перейти в справочник Бренды"""
        self.side_bar.check_brands_link()
        self.brands.check_page_loading()
