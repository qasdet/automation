from playwright.sync_api import Page

from admin_office.components.base_page import BasePage
from admin_office.components.models.ui.user_candidates.user_candidates import (
    UserCandidates,
)


class AdminOfficeUserCandidatesPage(BasePage):
    """Заявки"""

    def __init__(self, page: Page) -> None:
        super().__init__(page)

        self.user_candidates = UserCandidates(page)
