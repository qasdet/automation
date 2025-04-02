import json

import allure
import pytest

from db_stuff.db_interactions.campaigns_db_interactions import (
    get_campaigns_by_organization_id,
)
from db_stuff.db_interactions.organizations_db_interactions import (
    get_organization_by_email,
)
from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira
from user_office.constants import EMAIL_ORGANIZATION
from user_office.api_interactions.campaign.campaign_api_interactions import (
    CampaignsQueriesAPI,
)


@pytest.mark.usefixtures('authorization_in_user_office_with_token')
class TestCampaignsAPI:
    @staticmethod
    @pytest.mark.smoke()
    @allure.title('API тест списка кампаний по организации')
    @allure.story(jira.JIRA_LINK + 'MDP-4146')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.testcase(case.ALLURE_LINK + '121241?treeId=289')
    def test_get_list_campaigns_for_organization(
        authorization_in_user_office_with_token,
    ):
        token = authorization_in_user_office_with_token
        organization = get_organization_by_email(EMAIL_ORGANIZATION)
        campaigns_for_organization_db = get_campaigns_by_organization_id(
            organization.id
        )
        campaigns_for_organization_api = CampaignsQueriesAPI(
            token
        ).get_all_list_campaigns()
        campaigns_db_json = json.dumps(
            campaigns_for_organization_db, sort_keys=True
        )
        campaigns_api_json = json.dumps(
            campaigns_for_organization_api, sort_keys=True
        )
        assert (
            campaigns_db_json == campaigns_api_json
        ), 'Список кампаний через API не совпадает с ожидаемым из БД'
