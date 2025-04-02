from playwright.sync_api import Page

from user_office.components.base_page import BasePage


class StratPlansPage(BasePage):
    """Страница со списком страт-планов"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # TODO strategic_planning вынести в константу (MDP-4022)

    def visit_strat_plans_page(self, user_office_base_url: str) -> None:
        """Переход на страницу списка страт. планов"""
        self.visit(f'{user_office_base_url}/strategic-planning')
        self.page.wait_for_url('**/strategic-planning')

    def visit_specific_strat_plan_page(
        self, user_office_base_url: str, strat_plan_id: str
    ) -> None:
        """Переход на страницу конкретного страт. плана"""
        self.visit(
            f'{user_office_base_url}/strategic-planning/{strat_plan_id}'
        )
        self.page.wait_for_url(f'**/strategic-planning/{strat_plan_id}')
