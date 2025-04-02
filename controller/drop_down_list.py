import allure
from playwright.sync_api import Locator

from controller.factory import Factory


class DropDownList(Factory):
    def type_of(self) -> str:
        return 'DropDownList'

    def field_input(self, **kwargs) -> Locator:
        """Поле ввода"""
        locator = self.get_locator(**kwargs)
        return locator.locator("input:not([type='hidden'])")

    def fill(self, value: str, **kwargs: str) -> None:
        """Ввод текста"""
        with allure.step(f'Fill {self.type_of} {self.name} to value {value}'):
            self.field_input(**kwargs).fill(value)

    def select_item_by_text(self, name_item: str) -> None:
        """Выбрать запись
        Args:
            name_item: назввание записи
        """
        with allure.step(title=f'Выбрать запись с текстом {name_item}'):
            self.click()  # Открыть выпадающий список
            locator = self.get_locator()
            # locator.highlight()
            locator.get_by_text(name_item, exact=True).click()
            self.page.mouse.click(x=2, y=0)
            self.should_have_text(name_item)

    def should_have_item(self, name_item: str) -> None:
        """Проверка наличия элемента в выпадающем списке
        Args:
            name_item: назввание элемента списка
        """
        with allure.step(title=f'Выбрать запись с текстом {name_item}'):
            self.click()  # Открыть выпадающий список
            # Проверить доступность элемента перед его выбором
            self.page.get_by_role("option", name=f"{name_item}").is_visible()
            self.page.mouse.click(x=2, y=0)

    def __repr__(self):
        return self.locator