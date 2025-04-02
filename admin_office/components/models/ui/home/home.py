from playwright.sync_api import Page

from controller.button import Button


class Home:
    """Модель стартовой страницы"""

    def __init__(self, page: Page) -> None:
        self.sign_out = Button(
            page=page,
            locator="[data-testid='main_page_sign_out_button']",
            name='Выйти',
        )

    def check_page_loading(self) -> None:
        """Проверить загрузку страницы"""
        self.sign_out.should_be_visible()
