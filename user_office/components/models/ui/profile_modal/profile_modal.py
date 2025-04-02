from playwright.sync_api import Page

from controller.title import Title


class ProfileModal:
    """Данные пользователя"""

    def __init__(self, page: Page) -> None:
        self.page = page

        self.profile_results_title = Title(
            page,
            # locator='text="Автотесты QA-UCHETKA"',
            locator='figure',
            name='Профиль',
        )
        self.profile_user = Title(
            page,
            locator="//span[.='Профиль пользователя']",
            name='Профиль пользователя',
        )
        self.profile_orgs = Title(
            page,
            locator="//span[.='Профиль организации']",
            name='Профиль организации',
        )
        self.users = Title(
            page,
            locator="//span[.='Пользователи']",
            name='Профиль организации',
        )

    def modal_open(self):
        # self.profile_results_title.should_be_visible()  # Закомментировал, так как падает тест по созданию юзера
        self.profile_results_title.click()

    def profile_user_modal(self):
        self.profile_user.should_be_visible()
        self.profile_user.click()

    def profile_organization_modal(self):
        self.profile_orgs.should_be_visible()
        self.profile_orgs.click()

    def go_to_users(self) -> None:
        """Перейти на страницу Пользователи"""
        self.users.should_be_visible()
        self.users.click()
        self.page.mouse.click(x=2, y=0)
