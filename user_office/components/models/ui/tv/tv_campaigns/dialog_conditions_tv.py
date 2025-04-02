from playwright.sync_api import Page

from controller.input import Input
from modals.dialog_modal import DialogModal


class ConditionsTVModal(DialogModal):
    """Диалоговое окно Требования и ограничения"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.text_area = Input(
            page=page,
            locator="[data-testid='dialog_conditions_description']",
            name='Описание',
        )

    def fill(self, text: str) -> None:
        """Ввод текста в диалог Требования и ограничения
        Args:
            text: требования и ограничения
        """
        self.text_area.fill(text, validate_value=True)

    def fill_and_save_description(self, text: str) -> None:
        """Ввод текста и сохранение значения
        Args:
            text: требования и ограничения
        """
        self.fill(text)
        self.confirm()
