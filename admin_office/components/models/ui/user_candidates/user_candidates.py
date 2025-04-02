from playwright.sync_api import Page
from controller.table_new import Table


class UserCandidates:
    """Модель страницы Заявок"""

    def __init__(self, page: Page) -> None:
        self.page = page
        self.table = Table(
            page=page,
            locator="[data-testid='user_candidates_table']",
            name='Таблица Заявки',
        )

    def check_new_user_candidate(self, data_user_candidate: dict) -> None:
        """Проверяем созданную запись с таблице
        Args:
            data_user_candidate: Данные заявки
        """
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_user_candidate['id'],
            number_cell=0,
            check_text=data_user_candidate['id'],
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_user_candidate['id'],
            number_cell=1,
            check_text=data_user_candidate['name'],
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_user_candidate['id'],
            number_cell=2,
            check_text=data_user_candidate['surname'],
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_user_candidate['id'],
            number_cell=3,
            check_text=data_user_candidate['email'],
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_user_candidate['id'],
            number_cell=4,
            check_text=data_user_candidate['phone'],
        )
        self.table.should_have_text_cell_in_row_by_contains_text(
            text_row=data_user_candidate['id'],
            number_cell=6,
            check_text=data_user_candidate['comments'],
        )
