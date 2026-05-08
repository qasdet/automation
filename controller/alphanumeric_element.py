from playwright.sync_api import Locator, Page

from controller.factory import Factory


class AlphanumericElement(Factory):
    """Буквенно-цифровой элемент с поддержкой dynamic locators"""

    @property
    def type_of(self) -> str:
        return 'Alphanumeric Element'

    def __init__(self, page: Page, locator: str, name: str):
        super().__init__(page, locator, name)

    def get_locator(self, **kwargs) -> Locator:
        """Получить локатор с дефолтными значениями для contains_text и number_row"""
        kwargs['contains_text'] = kwargs.get('contains_text', '')
        kwargs['number_row'] = kwargs.get('number_row', 1)
        locator = self.locator.format(**kwargs)
        return self.page.locator(locator)
