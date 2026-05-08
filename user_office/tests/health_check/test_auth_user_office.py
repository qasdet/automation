import allure

from user_office.components.pages.authorization.authorization_page import (
    AuthorizationPage,
)
from user_office.components.pages.digital_page.digital_home_page import (
    DigitalHomePage,
)
from user_office.components.pages.profile.mediaplan_profile_page import (
    MediaPlanProfilePage,
)


class TestAuthUserOffice:
    """
    Набор тестов для проверки авторизации в UserOffice.

    Тестирует основные сценарии:
    - Проверка авторизации в UserOffice
    """

    @allure.title('Авторизация в Юзер Офисе')
    def test_auth_user_office(
        self,
        user_office_authorization: AuthorizationPage,
        digital_home_page: DigitalHomePage,
        mediaplan_profile_page: MediaPlanProfilePage,
        office_base_url: str,
    ):
        """
        Тест проверки авторизации в UserOffice.

        Проверяет:
        - Успешный переход на страницу авторизации
        - Успешную авторизацию в UserOffice
        """
        user_office_authorization.visit(office_base_url)
        user_office_authorization.authorize.auth_user_office()
