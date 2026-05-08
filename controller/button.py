import allure

from controller.factory import AssertableMixin, ClickableMixin, Factory


class Button(ClickableMixin, AssertableMixin, Factory):
    """
    Компонент для работы с кнопками.

    Наследует: ClickableMixin (click, hover, highlight),
    AssertableMixin (should_be_visible, should_be_enabled и т.д.).

    Использование:
        >>> button = Button(page, "[data-testid='submit']", "Отправить")
        >>> button.click().should_be_visible()
    """

    @property
    def type_of(self) -> str:
        """Тип компонента для логирования."""
        return 'button'

    def double_click(self, **kwargs) -> 'Button':
        """Двойной клик по кнопке."""
        with allure.step(f'Double clicking {self.type_of} "{self.name}"'):
            self.get_locator(**kwargs).dblclick()
        return self

    def right_click(self, **kwargs) -> 'Button':
        """Клик правой кнопкой мыши (контекстное меню)."""
        with allure.step(f'Right clicking {self.type_of} "{self.name}"'):
            self.get_locator(**kwargs).click(button='right')
        return self

    def click_and_hold(self, **kwargs) -> 'Button':
        """Клик с удержанием (для drag-and-drop)."""
        with allure.step(f'Click and hold {self.type_of} "{self.name}"'):
            self.get_locator(**kwargs).click(delay=100)
        return self

    def __repr__(self) -> str:
        return self.locator