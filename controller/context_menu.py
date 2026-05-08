import allure
from playwright.sync_api import Page

from controller.factory import AssertableMixin, ClickableMixin, Factory
from controller.list_item import ListItem


class ContextMenu(AssertableMixin, ClickableMixin, Factory):
    """
    Компонент для работы с контекстным меню.

    Attributes:
        item: Элемент меню для выполнения действий
    """

    @property
    def type_of(self) -> str:
        """Тип компонента для логирования."""
        return 'context menu'

    def __init__(self, page: Page, locator: str, name: str) -> None:
        super().__init__(page, locator, name)
        self.item = ListItem(
            page,
            locator=self.locator + "//mts-menu-item['{action}']",
            name='Действие',
        )

    def click_item(self, action: str) -> 'ContextMenu':
        """Кликнуть по пункту меню."""
        with allure.step(f'Clicking menu item "{action}"'):
            self.item.get_locator(action=action).click()
        return self
