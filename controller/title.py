import allure
import logging

from controller.factory import Factory
from playwright.sync_api import expect, Locator


"""Компонент для обработки заголовков/текста"""


class Title(Factory):
    @property
    def type_of(self) -> str:
        return 'title'

    def should_have_text(self, text: str, **kwargs):
        """Проверка видимости текста заголовка на странице

                Args:
                    text (str): текст заголовка
                """
        with allure.step(
                title=f'Checking that {self.type_of} "{self.name}" has text "{text}"'
        ):
            locator: Locator = self.get_locator(**kwargs)
            logging.info(
                f'Checking that {self.type_of} "{self.name}" has text "{text}"'
            )
            expect(actual=locator).to_have_text(expected=text)
            assert locator.is_visible()

    def has_texts(self, text: str, **kwargs):
        locator = self.get_locator(**kwargs)
        expect(locator).to_contain_text(text)

    def __repr__(self):
        return self.locator
