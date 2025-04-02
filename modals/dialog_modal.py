from playwright.sync_api import Page
from controller.button import Button
from controller.title import Title


class DialogModal:
    """Диалоговое окно"""

    def __init__(self, page: Page) -> None:
        self.page = page

        self.title = Title(
            page,
            locator="[data-testid='dialog_title']",
            name='Заголовок',
        )
        self.cancel_button = Button(
            page,
            locator="[data-testid='dialog_cancel']",
            name='Кнопка Отмены',
        )
        self.confirm_button = Button(
            page,
            locator="[data-testid='dialog_confirm']",
            name='Кнопка Подтверждения',
        )

    def confirm(self) -> None:
        """Подтверждение"""
        self.confirm_button.click()
        self.confirm_button.should_be_not_visible()

    def cancel(self) -> None:
        """Отмена"""
        self.cancel_button.click()
        self.cancel_button.should_be_not_visible()

    def check_dialog_visible(self) -> None:
        """Проверяем, что диалоговое окно отображается"""
        self.title.should_be_visible()
