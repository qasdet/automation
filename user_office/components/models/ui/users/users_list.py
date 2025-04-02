from playwright.sync_api import Page
from controller.button import Button
from controller.table_new import Table


class UsersList:
    """Модель страницы Пользователей в user office"""

    def __init__(self, page: Page) -> None:
        self.create_button = Button(
            page=page,
            locator="//button[.='Создать']",
            name='Создать пользователя',
        )
        self.table = Table(
            page=page,
            locator='table',
            name='Таблица пользователей',
        )

    def open_the_user_creation_form(self) -> None:
        """Открыть форму создания тв кампании"""
        self.create_button.click()

    def open_the_user_for_editing(self, text_row: str) -> None:
        """Открыть форму создания пользователя

        Args:
            text_row: текст строки
        """
        self.table.open_menu_action_in_row_by_contains_text(text_row)
        self.table.click_item_menu_action('Редактировать')

    def check_visible_new_user(self, **kwargs) -> None:
        """Проверка отображения новой записи"""

        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=kwargs['login'], number_cell=0, check_text=kwargs['login']
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=kwargs['login'],
            number_cell=1,
            check_text=kwargs['surname'],
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=kwargs['login'], number_cell=2, check_text=kwargs['name']
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=kwargs['login'],
            number_cell=3,
            check_text=kwargs['middle_name'],
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=kwargs['login'], number_cell=4, check_text=kwargs['email']
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=kwargs['login'], number_cell=5, check_text=kwargs['phone']
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=kwargs['login'], number_cell=6, check_text=kwargs['role']
        )
