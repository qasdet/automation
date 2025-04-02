import allure

from controller.factory import Factory

"""Компонент для кнопок"""


class Button(Factory):
    @property
    def type_of(self) -> str:
        """Функция type_of возвращает наименование компонента для отчетности в аллюр"""
        return 'button'

    def hover(self, **kwargs) -> None:
        """Общий метод наведения на объект страницы/локатор"""
        with allure.step(
            f'Hovering over {self.type_of} with name "{self.name}"'
        ):
            locator = self.get_locator(**kwargs)
            locator.hover()

    def double_click(self, **kwargs):
        """Общий метод двойного клика на объект страницы/локатор"""
        with allure.step(f'Double clicking {self.type_of} with "{self.name}"'):
            locator = self.get_locator(**kwargs)
            locator.dblclick()

    def __repr__(self):
        return self.locator