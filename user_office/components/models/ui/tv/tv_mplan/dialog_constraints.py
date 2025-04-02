from playwright.sync_api import Page

from modals.dialog_modal import DialogModal


class ConstraintsProductTVModal(DialogModal):
    """Диалоговое окно Задачи и ограничения продукта"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)
