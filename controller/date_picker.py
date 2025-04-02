import allure
from playwright.sync_api import Locator, expect

from controller.drop_down_list import DropDownList


class DatePicker(DropDownList):
    """Компонент для поля дат"""

    @property
    def type_of(self) -> str:
        return 'date picker'

    # TODO: Rename input method to field_input
    def input(self, **kwargs: str) -> Locator:
        """Поле ввода"""
        date_picker = self.get_locator(**kwargs)
        return date_picker.locator('input')

    def fill(self, value: str, **kwargs: str) -> None:
        """Ввод текста"""
        with allure.step(f'Fill {self.type_of} {self.name} to value {value}'):
            self.input(**kwargs).fill(value)

    def should_have_value(self, value: str, **kwargs: str) -> None:
        """Проверка, что поле имеет указанное значение"""
        with allure.step(
            f'Checking {self.type_of} {self.name} has a value {value}'
        ):
            expect(self.input(**kwargs)).to_have_value(value)

    def __repr__(self):
        return self.locator