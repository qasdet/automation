# TODO Закомментированный код необходимо актуализировать
import pytest
from faker import Faker
from playwright.sync_api import Page

from admin_office.components.pages.authorization.authorization_page import (
    AdminOfficeAuthorizationPage,
)
from admin_office.components.pages.brands.brands_page import (
    AdminOfficeBrandsPage,
)
from admin_office.components.pages.channels.channels_page import (
    AdminOfficeChannelsPage,
)
from admin_office.components.pages.clients.clients_page import (
    AdminOfficeClientsPage,
)
from admin_office.components.pages.home.home_page import AdminOfficeHomePage
from admin_office.components.pages.instruments.instruments_page import AdminOfficeInstrumentsPage
from admin_office.components.pages.organizations.organizations_page import (
    AdminOfficeOrganizationsPage,
)
from admin_office.components.pages.placement_statuses.placement_statuses_page import (
    AdminOfficePlacementStatusesPage,
)
from admin_office.components.pages.product_price_categories.product_price_categories_page import (
    AdminOfficeProductPriceCategoriesPage,
)
from admin_office.components.pages.products.products_page import (
    AdminOfficeProductsPage,
)
from admin_office.components.pages.user_candidates.user_candidates_page import (
    AdminOfficeUserCandidatesPage,
)
from admin_office.components.pages.sources.sources_page import (
    AdminOfficeSourcesPage,
)
from admin_office.components.pages.users.users_page import AdminOfficeUsersPage
from admin_office.api_interactions.channels.channels_api_interactions import (
    create_channel_api,
)
from admin_office.tests.api.dictionaries.channels.data_generator_for_channel import (
    get_data_for_channel,
)
from db_stuff.db_interactions.channels_db_interactions import (
    delete_channel_by_naming,
    get_channel_by_naming,
)

faker = Faker()


@pytest.fixture(scope='module')
def admin_home_page(chromium_page: Page) -> AdminOfficeHomePage:
    return AdminOfficeHomePage(chromium_page)


@pytest.fixture(scope='module')
def admin_office_authorization(
    chromium_page: Page,
) -> AdminOfficeAuthorizationPage:
    return AdminOfficeAuthorizationPage(chromium_page)


@pytest.fixture(scope='function')
def admin_organizations_page(
    chromium_page: Page,
) -> AdminOfficeOrganizationsPage:
    return AdminOfficeOrganizationsPage(chromium_page)


@pytest.fixture(scope='function')
def admin_users_page(chromium_page: Page) -> AdminOfficeUsersPage:
    return AdminOfficeUsersPage(chromium_page)


@pytest.fixture(scope='function')
def admin_brands_page(chromium_page: Page) -> AdminOfficeBrandsPage:
    return AdminOfficeBrandsPage(chromium_page)


@pytest.fixture(scope='function')
def admin_products_page(chromium_page: Page) -> AdminOfficeProductsPage:
    return AdminOfficeProductsPage(chromium_page)


@pytest.fixture(scope='function')
def admin_clients_page(chromium_page: Page) -> AdminOfficeClientsPage:
    return AdminOfficeClientsPage(chromium_page)


@pytest.fixture(scope='function')
def admin_sources_page(chromium_page: Page) -> AdminOfficeSourcesPage:
    return AdminOfficeSourcesPage(chromium_page)


@pytest.fixture(scope='function')
def admin_instruments_page(chromium_page: Page) -> AdminOfficeInstrumentsPage:
    return AdminOfficeInstrumentsPage(chromium_page)


@pytest.fixture(scope='function')
def admin_user_candidates_page(
    chromium_page: Page,
) -> AdminOfficeUserCandidatesPage:
    return AdminOfficeUserCandidatesPage(chromium_page)


@pytest.fixture(scope='function')
def admin_placement_statuses_page(
    chromium_page: Page,
) -> AdminOfficePlacementStatusesPage:
    return AdminOfficePlacementStatusesPage(chromium_page)


@pytest.fixture(scope='function')
def admin_product_price_categories_page(
    chromium_page: Page,
) -> AdminOfficeProductPriceCategoriesPage:
    return AdminOfficeProductPriceCategoriesPage(chromium_page)


@pytest.fixture(scope='function')
def admin_channels_page(
    chromium_page: Page,
) -> AdminOfficeChannelsPage:
    return AdminOfficeChannelsPage(chromium_page)


@pytest.fixture(scope='module')
def authorization_in_admin_office(
    admin_base_url: str,
    admin_office_authorization: AdminOfficeAuthorizationPage,
    admin_home_page: AdminOfficeHomePage,
):
    admin_office_authorization.visit(admin_base_url)
    admin_office_authorization.authorization.auth_admin_office()
    admin_home_page.home.check_page_loading()


@pytest.fixture(scope='module')
def authorization_in_admin_office_with_token(
    admin_base_url: str,
    admin_api_auth_url: str,
    admin_office_authorization: AdminOfficeAuthorizationPage,
    admin_home_page: AdminOfficeHomePage,
) -> str:
    """Авторизация Admin office с получением токена
    Return:
        Возвращаем заголовок с токеном доступа
    """
    admin_office_authorization.visit(admin_base_url)
    with admin_office_authorization.page.expect_request(
        lambda request: request.url == admin_api_auth_url
    ) as first:
        admin_office_authorization.authorization.auth_admin_office()
        admin_home_page.home.check_page_loading()
    first_request = first.value
    access_token = first_request.response().json()['account']['access_token']
    yield {'admin-authorization': f'Bearer {access_token}'}


@pytest.fixture()
def life_cycle_of_the_channel(
    authorization_in_admin_office_with_token,
) -> dict:
    """Создание и удаление канала"""
    token = authorization_in_admin_office_with_token
    data_channel = get_data_for_channel()
    create_channel_api(**data_channel, token=token)
    yield data_channel, token
    channel = get_channel_by_naming(data_channel['naming'])
    if channel:
        delete_channel_by_naming(channel.naming)
