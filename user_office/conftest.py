import time
import pytest

from faker import Faker
from playwright.sync_api import Page
from admin_office.api_interactions.clients.clients_api_interactions import create_client_user_office
from admin_office.api_interactions.brands.brands_api_interactions import brand_creation
from admin_office.api_interactions.products.products_api_interactions import create_product_user_office
from helper.names_generator.brand_names_generator import brand_data_generator
from helper.names_generator.client_names_generator import client_data_generator
from helper.names_generator.product_names_generator import product_data_generator
from user_office.components.pages.authorization.authorization_page import (
    AuthorizationPage,
)
from user_office.components.pages.campaigns.about_campaign_page import (
    AboutCampaignPage,
)
from user_office.components.pages.campaigns.campaign_page import CampaignPage
from user_office.components.pages.campaigns.campaigns_list_page import (
    CampaignsListPage,
)
from user_office.components.pages.campaigns.create_campaign_page import (
    CreateCampaignPage,
)
from user_office.components.pages.digital_page.digital_home_page import (
    DigitalHomePage,
)
from user_office.components.pages.dictionaries.dictionaries_page import (
    DictionariesPage,
)
from user_office.components.pages.health_check.health_check_page import (
    HealthCheckPage,
)
from user_office.components.pages.mediaplan.create_mediaplan_page import (
    CreateMediaplanPage,
)
from user_office.components.pages.mediaplan.mediaplan_page import MediaplanPage
from user_office.components.pages.placement.placement_page import PlacementPage
from user_office.components.pages.profile.mediaplan_profile_page import (
    MediaPlanProfilePage,
)
from user_office.components.pages.reporting.reporting_page import ReportingPage
from user_office.components.pages.users.user_card_page import UserCardPage
from user_office.components.pages.users.users_page import UsersPage

faker = Faker()


@pytest.fixture(scope='module')
def authorization_in_user_office(
        office_base_url: str,
        user_office_authorization: AuthorizationPage,
):
    user_office_authorization.visit(office_base_url)
    user_office_authorization.authorize.auth_user_office()


@pytest.fixture(scope='module')
def authorization_in_user_office_with_token(
        office_base_url: str,
        user_office_gateway_auth_url: str,
        user_office_authorization: AuthorizationPage,
):
    user_office_authorization.page.goto(office_base_url, wait_until="load")
    user_office_authorization.authorize.auth_user_office()
    time.sleep(15)
    result = user_office_authorization.page.request.get(user_office_gateway_auth_url)
    token = result.json()['account']['access_token']
    yield {'authorization': f'Bearer {token}'}


@pytest.fixture(scope='function')
def dictionaries(chromium_page: Page) -> DictionariesPage:
    return DictionariesPage(chromium_page)


@pytest.fixture(scope='function')
def campaign_page(chromium_page: Page) -> CampaignPage:
    return CampaignPage(chromium_page)


@pytest.fixture(scope='function')
def instruction(chromium_page: Page) -> CampaignPage:
    return CampaignPage(chromium_page)


@pytest.fixture(scope='function')
def campaigns_list_page(chromium_page: Page) -> CampaignsListPage:
    return CampaignsListPage(chromium_page)


@pytest.fixture(scope='function')
def create_campaign_page(chromium_page: Page) -> CreateCampaignPage:
    return CreateCampaignPage(chromium_page)


@pytest.fixture(scope='function')
def about_campaign_page(chromium_page: Page) -> AboutCampaignPage:
    return AboutCampaignPage(chromium_page)


@pytest.fixture(scope='module')
def user_office_authorization(chromium_page: Page) -> AuthorizationPage:
    return AuthorizationPage(chromium_page)


@pytest.fixture(scope='function')
def digital_home_page(chromium_page: Page) -> DigitalHomePage:
    return DigitalHomePage(chromium_page)


@pytest.fixture(scope='function')
def mediaplan_page(chromium_page: Page) -> MediaplanPage:
    return MediaplanPage(chromium_page)


@pytest.fixture(scope='function')
def create_mediaplan_page(chromium_page: Page) -> CreateMediaplanPage:
    return CreateMediaplanPage(chromium_page)


@pytest.fixture(scope='function')
def mediaplan_profile_page(chromium_page: Page) -> MediaPlanProfilePage:
    return MediaPlanProfilePage(chromium_page)


@pytest.fixture(scope='function')
def health_check_page(chromium_page: Page) -> HealthCheckPage:
    return HealthCheckPage(chromium_page)


@pytest.fixture(scope='function')
def placement_page(chromium_page: Page) -> PlacementPage:
    return PlacementPage(chromium_page)


@pytest.fixture(scope='function')
def reporting_page(chromium_page: Page) -> ReportingPage:
    return ReportingPage(chromium_page)


@pytest.fixture(scope='function')
def users_page(chromium_page: Page) -> UsersPage:
    return UsersPage(chromium_page)


@pytest.fixture(scope='function')
def user_card_page(chromium_page: Page) -> UserCardPage:
    return UserCardPage(chromium_page)


@pytest.fixture(scope='function')
def create_client_brand_product_data_through_user_office_api(
        authorization_in_user_office_with_token: str,
) -> dict:
    """
        Фикстура создаёт связку клиент-бренд-продукт для дальнейшего использования в тестах. Создание происходит через
        api-методы для user-office.
    Args:
        authorization_in_user_office_with_token: Нужен для авторизации в user-office
    Returns:
        Возвращает словарь, который содержит три id: клиента, бренда и продукта. Далее, можно по этим id дёргать доп.
        данные по клиенту, бренду и продукту.
    """
    client_data_dict = client_data_generator()
    user_office_authorization_token = authorization_in_user_office_with_token
    client_created_id = create_client_user_office(
        client_data_dict, user_office_authorization_token
    )
    brand_data_dict = brand_data_generator(client_created_id)
    brand_created_id = brand_creation(
        brand_data_dict, user_office_authorization_token
    )
    product_data_dict = product_data_generator(
        client_created_id, brand_created_id
    )
    product_created_id = create_product_user_office(
        product_data_dict, user_office_authorization_token
    )
    dictionary_with_results = {
        'client_id': client_created_id,
        'brand_id': brand_created_id,
        'product_id': product_created_id,
    }
    yield dictionary_with_results
