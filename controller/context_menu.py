from playwright.sync_api import Page

from controller.factory import Factory
from controller.list_item import ListItem


class ContextMenu(Factory):
    @property
    def type_of(self) -> str:
        return 'context menu'

    def __init__(self, page: Page, locator: str, name: str):
        super().__init__(page, locator, name)
        self.item = ListItem(
            page,
            locator=self.locator + "//mts-menu-item['{action}']",
            name='Действие',
        )