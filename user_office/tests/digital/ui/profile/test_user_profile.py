import pytest

from user_office.components.pages.digital_page.digital_home_page import (
    DigitalHomePage,
)
from user_office.components.pages.profile.mediaplan_profile_page import (
    MediaPlanProfilePage,
)


@pytest.mark.usefixtures('authorization_in_user_office')
class TestProfile:
    @staticmethod
    def test_profile(
        digital_home_page: DigitalHomePage,
        mediaplan_profile_page: MediaPlanProfilePage,
    ):
        digital_home_page.navbar.profile_open()
        mediaplan_profile_page.navbar.profile_user()
