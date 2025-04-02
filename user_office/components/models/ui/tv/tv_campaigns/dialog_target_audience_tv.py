from playwright.sync_api import Page

from controller.input import Input
from modals.dialog_modal import DialogModal


class TargetAudienceTVModal(DialogModal):
    """Диалоговое окно Целевая аудитория"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.text_area = Input(
            page=page,
            locator="[data-testid='dialog_target_audience_description']",
            name='Описание',
        )

    def fill(self, text: str) -> None:
        """Ввод текста в диалог Целевая аудитория
        Args:
            text: целевая аудитория
        """
        self.text_area.fill(text, validate_value=True)

    def fill_and_save_description(self, text: str) -> None:
        """Ввод текста и сохранение значения
        Args:
            text: целевая аудитория
        """
        self.fill(text)
        self.confirm()
