import pytest

from user_office.components.pages.authorization.authorization_page import (
    AuthorizationPage,
)
from user_office.components.pages.digital_page.digital_home_page import (
    DigitalHomePage,
)
from user_office.components.pages.profile.mediaplan_profile_page import (
    MediaPlanProfilePage,
)


@pytest.mark.usefixtures('authorization_in_user_office')
class TestProfile:
    def test_profile(
        self,
        user_office_authorization: AuthorizationPage,
        digital_home_page: DigitalHomePage,
        mediaplan_profile_page: MediaPlanProfilePage,
        base_url,
    ):
        digital_home_page.navbar.profile_open()
        mediaplan_profile_page.navbar.profile_user()
