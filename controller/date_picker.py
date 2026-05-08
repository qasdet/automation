import allure
from playwright.sync_api import Locator

from controller.drop_down_list import DropDownList


class DatePicker(DropDownList):
    """Компонент для работы с полями выбора даты (date picker)."""

    @property
    def type_of(self) -> str:
        """Тип компонента для логирования."""
        return 'date picker'

    def input(self, **kwargs) -> Locator:
        """Получить локатор поля ввода даты внутри компонента."""
        return self.get_locator(**kwargs).locator('input')

    def fill(self, value: str, **kwargs) -> 'DatePicker':
        """Заполнить поле даты указанным значением."""
        with allure.step(f'Filling {self.type_of} "{self.name}" with "{value}"'):
            self.input(**kwargs).fill(value)
        return self
