from playwright.sync_api import Page

from controller.title import Title


class HealthUserOffice:
    """Модель страницы для теста health check"""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.title_digital = Title(
            page, locator="//a[.='Digital кампании']", name='Digital'
        )
        self.title_tv = Title(page, locator="//a[.='ТВ кампании']", name='TV')
        self.media = Title(page, locator="text='Медиа'", name='Медиа')
        self.campaign = Title(page, locator="text='Кампания'", name='Кампания')
        self.client = Title(page, locator="text='Клиент'", name='Клиент')
        self.product_brand_and_co_brand = Title(
            page,
            locator="text='Продукт, бренд и ко-бренд'",
            name='Продукт, бренд и ко-бренд',
        )
        self.change = Title(
            page, locator="text='Дата изменения'", name='Дата изменения'
        )
        self.status = Title(page, locator="text='Статус'", name='Статус')

    def check_media(self):
        # self.media.should_be_visible()
        self.media.matching_by_text(text='Медиа')

    def check_campaign(self):
        self.campaign.should_be_visible()
        self.campaign.matching_by_text(text='Кампания')

    def check_client(self):
        # self.client.should_be_visible()
        self.client.matching_by_text(text='Клиент')

    def check_product_brand_and_co_brand(self):
        # self.product_brand_and_co_brand.should_be_visible()
        self.product_brand_and_co_brand.matching_by_text(text='Продукт, бренд и ко-бренд')

    def check_change(self):
        # self.change.should_be_visible()
        self.change.matching_by_text(text='Дата изменения')

    def check_status(self):
        # self.status.should_be_visible()
        self.status.matching_by_text(text='Статус')

    def click_digital(self):
        self.title_digital.should_be_visible()
        self.title_digital.click()

    def click_tv(self):
        self.title_tv.should_be_visible()
        self.title_tv.click()

    def check_all_text(self):
        self.check_media()
        self.check_campaign()
        self.check_client()
        self.check_product_brand_and_co_brand()
        self.check_change()
        self.check_status()
        self.click_digital()
        # self.click_tv()
