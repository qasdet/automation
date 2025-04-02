import allure
from playwright.sync_api import expect

from controller.factory import Factory

"""Компонент для полей ввода"""


class Input(Factory):
    @property
    def type_of(self) -> str:
        return 'input'

    def fill(
        self, value: str, validate_value: object = False, **kwargs: object
    ) -> object:
        with allure.step(
            f'Fill {self.type_of} "{self.name}" to value "{value}"'
        ):
            locator = self.get_locator(**kwargs)
            locator.fill(value)
            locator.highlight()
            if validate_value:
                self.should_have_value(value, **kwargs)

    def fill_by_label(
        self,
        label_value: str,
        value_to_fill: str,
        validate_value: object = False,
        **kwargs: object,
    ) -> object:
        with allure.step(
            f'Fill {self.type_of} "{self.name}" to value "{label_value}"'
        ):
            locator = self.get_locator(**kwargs)
            locator.page.get_by_label(label_value).fill(value_to_fill)
            locator.highlight()
            if validate_value:
                self.should_have_value(value_to_fill, **kwargs)

    # TODO: Позже доработаю заполнение плейсхолдеров, для конверсий
    # def fill_placeholder(self, value: str, **kwargs):
    #     with allure.step(f'Fill {self.type_of} "{self.name}" to value "{value}"'):
    #         locator = self.get_locator(**kwargs)
    #         locator.get_by_placeholder(value).fill(value)

    def should_have_value(self, value: str | float, **kwargs):
        with allure.step(
            f'Checking {self.type_of} {self.name}" has a value "{value}"'
        ):
            locator = self.get_locator(**kwargs)
            locator.highlight()
            expect(locator).to_have_value(value)
