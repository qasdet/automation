from playwright.sync_api import Page

from controller.button import Button
from controller.table_new import Table
from controller.title import Title
from modals.dialog_modal import DialogModal


class StratPlanGeneral:
    """Модель страницы списка стратегических планов"""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.title = Title(
            page,
            locator='.css-1ylyj51',
            name='Стратегическое планирование',
        )
        self.create_strat_plan_button = Button(
            page, locator='text="Создать"', name='Создать'
        )
        self.table = Table(
            page=page, locator='//table', name='Таблица кампаний'
        )
        self.confirm_window = DialogModal(page=page)

    def click_create_strat_plan_button(self) -> None:
        """Нажатие на кнопку создания страт плана"""
        self.create_strat_plan_button.click()

    def click_ok_button_in_strat_plan_confirm_dialog(self) -> None:
        """Подтверждение удаления страт-плана"""
        self.confirm_window.confirm()

    def click_cancel_button_in_strat_plan_confirm_dialog(self) -> None:
        """Отмена в окне подтверждения удаления страт-плана"""
        self.confirm_window.cancel()
