from playwright.sync_api import expect

from controller.factory import Factory


class Tabbar(Factory):
    def type_of(self) -> str:
        return 'tabbar'

    def select_tab_by_text(self, name_tab, **kwargs) -> None:
        """Выбрать вкладку в tabbar по тексту
        Args:
            name_tab: название вкладки
        """
        locator = self.get_locator(**kwargs)
        locator.get_by_text(name_tab).click()

    def should_be_visible_tab_by_text(self, name_tab, **kwargs) -> None:
        """Проверка, что вкладка с указанным текстом отображается
        Args:
            name_tab: название вкладки
        """
        locator = self.get_locator(**kwargs)
        expect(locator.get_by_text(name_tab)).to_be_visible()

    def should_be_active_tab_by_text(self, name_tab, **kwargs) -> None:
        """Проверка, что вкладка с указанным текстом выбрана
        Args:
            name_tab: название вкладки
        """
        # TODO Уточнить признак, что вкладка является активной
        locator = self.get_locator(**kwargs)
        expect(locator.locator('.css-lt7pxj').locator('a')).to_have_text(
            name_tab
        )

    def __repr__(self):
        return self.locator
