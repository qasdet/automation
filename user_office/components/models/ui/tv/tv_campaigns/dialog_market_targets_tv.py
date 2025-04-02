from playwright.sync_api import Page

from controller.input import Input
from modals.dialog_modal import DialogModal


class MarketTargetsTVModal(DialogModal):
    """Диалоговое окно Цели рекламной кампании"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.text_area = Input(
            page=page,
            locator="[data-testid='dialog_market_targets_description']",
            name='Описание',
        )

    def fill(self, text: str) -> None:
        """Ввод текста в диалог Цели рекламной кампании
        Args:
            text: цели рекламной кампании
        """
        self.text_area.fill(text, validate_value=True)

    def fill_and_save_description(self, text: str) -> None:
        """Ввод текста и сохранение значения
        Args:
            text: цели рекламной кампании
        """
        self.fill(text)
        self.confirm()
