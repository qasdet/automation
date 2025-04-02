import allure
import pytest

from admin_office.components.pages.organizations.organizations_page import (
    AdminOfficeOrganizationsPage,
)
from admin_office.constants import LIMIT_OF_ROWS_ON_ONE_PAGE_IN_ORGANIZATIONS
from admin_office.api_interactions.organizations.organization_api_interactions import (
    get_count_of_organizations,
)
from admin_office.tests.api.organizations.data_make_for_organization import (
    make_data_all_legal_entity_fields,
    make_the_expected_data_for_ui,
)
from db_stuff.db_interactions.organizations_db_interactions import (
    delete_organization_by_id,
    get_organization_by_inn_and_kpp,
)
from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira


@pytest.fixture()
def life_cycle_of_the_organization_with_all_field():
    data_organization = make_data_all_legal_entity_fields()
    yield data_organization
    organization = get_organization_by_inn_and_kpp(
        data_organization['inn'], data_organization['kpp']
    )
    if organization:
        delete_organization_by_id(organization.id)


@pytest.mark.usefixtures('authorization_in_admin_office_with_token')
class TestsOrganizations:
    @staticmethod
    @pytest.mark.smoke
    @allure.title('Страница Организации')
    @allure.story(jira.JIRA_LINK + 'MDP-181')
    @allure.testcase(case.ALLURE_LINK + '124593')
    def test_view_organizations(
        admin_organizations_page: AdminOfficeOrganizationsPage,
        authorization_in_admin_office_with_token: str,
    ):
        """Страница Организации"""
        token = authorization_in_admin_office_with_token
        admin_organizations_page.go_to_organizations()
        count_all_rows = get_count_of_organizations(token)
        admin_organizations_page.organizations.check_quantity_organizations(
            count_all_rows
        )
        admin_organizations_page.organizations.check_transition_to_next_page(
            count_all_rows
        )
        count_rows_in_second_page = (
            count_all_rows
            if count_all_rows <= LIMIT_OF_ROWS_ON_ONE_PAGE_IN_ORGANIZATIONS
            else count_all_rows - LIMIT_OF_ROWS_ON_ONE_PAGE_IN_ORGANIZATIONS
        )
        admin_organizations_page.organizations.check_quantity_organizations(
            count_rows_in_second_page
        )

    @staticmethod
    @pytest.mark.smoke
    @allure.title('Добавление организации')
    @allure.story(jira.JIRA_LINK + 'MDP-181')
    @allure.testcase(case.ALLURE_LINK + '131193')
    def test_create_organization(
        admin_organizations_page: AdminOfficeOrganizationsPage,
        life_cycle_of_the_organization_with_all_field,
    ):
        """Добавление организации"""
        data_organization = life_cycle_of_the_organization_with_all_field
        admin_organizations_page.go_to_organizations()
        admin_organizations_page.organizations.open_the_organization_creation_form()
        admin_organizations_page.card_organization.fill_all_fields(
            data_organization
        )
        expected_data = make_the_expected_data_for_ui(data_organization)
        admin_organizations_page.card_organization.save_organization()
        admin_organizations_page.organizations.check_new_organization(
            expected_data
        )
