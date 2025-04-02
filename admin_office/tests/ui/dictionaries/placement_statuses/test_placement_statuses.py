import allure
import pytest

from admin_office.components.pages.placement_statuses.placement_statuses_page import (
    AdminOfficePlacementStatusesPage,
)
from db_stuff.db_interactions.placement_statuses_db_interactions import (
    get_list_of_the_placement_statuses_from_db,
)
from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira


@pytest.mark.usefixtures('authorization_in_admin_office')
class TestsPlacementStatusesUI:
    @staticmethod
    @pytest.mark.regress()
    @allure.title('Справочник Статусы размещений')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.story(jira.JIRA_LINK + 'MDP-903')
    @allure.testcase(case.ALLURE_LINK + '149509')
    def test_view_placement_statuses(
        admin_placement_statuses_page: AdminOfficePlacementStatusesPage,
    ) -> None:
        """Справочник Статусы размещений"""

        admin_placement_statuses_page.go_to_placement_statuses()
        placement_statuses_db = get_list_of_the_placement_statuses_from_db()
        for index, row_db in enumerate(placement_statuses_db):
            admin_placement_statuses_page.placement_statuses.table.should_have_text_cell_in_row_by_contains_text(
                text_row=str(row_db['id']),
                number_cell=0,
                check_text=str(row_db['id']),
            )
            admin_placement_statuses_page.placement_statuses.table.should_have_text_cell_in_row_by_contains_text(
                text_row=str(row_db['id']),
                number_cell=1,
                check_text=row_db['name'],
            )
            admin_placement_statuses_page.placement_statuses.table.should_have_text_cell_in_row_by_contains_text(
                text_row=str(row_db['id']),
                number_cell=2,
                check_text=row_db['code'],
            )
