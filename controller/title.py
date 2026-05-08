import allure
from playwright.sync_api import expect

from controller.factory import AssertableMixin, Factory


class Title(AssertableMixin, Factory):
    """Компонент для работы с заголовками и текстовыми элементами."""

    @property
    def type_of(self) -> str:
        """Тип компонента для логирования."""
        return 'title'

    def should_contain_text(self, text: str, **kwargs) -> 'Title':
        """Проверить, что текст заголовка содержит указанную подстроку."""
        with allure.step(f'Checking {self.type_of} "{self.name}" contains text "{text}"'):
            expect(self.get_locator(**kwargs)).to_contain_text(text)
        return self
