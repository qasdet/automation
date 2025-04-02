from playwright.sync_api import Page

from controller.button import Button
from controller.factory import Factory


class Paging(Factory):
    def type_of(self) -> str:
        return 'Paging'

    def __init__(self, page: Page, locator: str, name: str):
        super().__init__(page, locator, name)
        self.prev_button = Button(
            self.page,
            locator=f'{locator}//button[1]',
            name='Предыдущая страница',
        )
        self.next_button = Button(
            self.page,
            locator=f'{locator}//button[2]',
            name='Следующая страница',
        )

    def go_to_next_page(self):
        """Переход к следующей странице"""
        self.next_button.should_be_visible()
        self.next_button.click()

    def go_to_prev_page(self):
        """Переход к предыдущей странице"""
        self.prev_button.should_be_visible()
        self.prev_button.click()
