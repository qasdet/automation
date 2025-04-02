import pytest

from playwright.sync_api import Page
from admin_office.components.pages.landing.landing_page import LandingPage


@pytest.fixture(scope='function')
def landing_page(chromium_page: Page) -> LandingPage:
    return LandingPage(chromium_page)
