import time
import allure
import pytest

from datetime import datetime, timedelta
from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira
from user_office.api_interactions.campaign.campaign_api_interactions import CampaignsMutationsAPI
from user_office.api_interactions.connections.connections_api_interactions import ConnectionSettingsMutationsAPI
from user_office.api_interactions.mediaplan.mediaplan_api_interactions import MplansMutationsAPI
from user_office.api_interactions.placement.placement_api_interactions import PlacementMutationsAPI, PlacementQueriesAPI
from user_office.api_interactions.reporting.reporting_api_interactions import ReportingQueriesAPI
from user_office.components.pages.reporting.reporting_page import ReportingPage
from db_stuff.db_interactions.digital_reports_db_interactions import get_digital_report_by_campaign_id
from helper.reporting_data_handlers import reporting_data_handler_db, reporting_data_handler_api
from helper.default_dates import get_default_campaign_begin_date_for_api, get_default_campaign_end_date_for_api, \
    get_default_campaign_begin_date_for_ui, get_default_campaign_end_date_for_ui
from user_office.api_interactions.targeting.targeting_api_interactions import TargetingMutationsAPI


@pytest.mark.usefixtures('authorization_in_user_office_with_token')
class TestReportingDataAPI:

    @staticmethod
    @allure.story(jira.JIRA_LINK + 'MDP-5321')
    @allure.testcase(case.ALLURE_LINK + '405705?treeId=289')
    @allure.title('API тест данных отчета План-факт')
    @allure.description(
        'API тест данных отчета План-факт'
    )
    @pytest.mark.regress
    @allure.severity(allure.severity_level.NORMAL)
    def test_reporting_data(
            reporting_page: ReportingPage,
            digital_test_data,
            authorization_in_user_office_with_token,
            office_base_url: str,
    ):
        campaign_id = CampaignsMutationsAPI(authorization_in_user_office_with_token).create_campaign_full(
            digital_test_data
        )
        mplan_data = MplansMutationsAPI(authorization_in_user_office_with_token).create_mplan_part(
            campaign_id
        )
        placement_data = PlacementMutationsAPI(authorization_in_user_office_with_token).create_placement_part_mts_dsp(
            mplan_data['data']['mplanPlanningCreate']['id'], digital_test_data
        )
        TargetingMutationsAPI(authorization_in_user_office_with_token).add_targeting_descriptions(
            placement_data['data']['placementCreate']['id'],
        )
        metrics_and_conv_data = PlacementQueriesAPI(
            authorization_in_user_office_with_token).get_metrics_and_conversions(
            mplan_data['data']['mplanPlanningCreate']['id'], placement_data['data']['placementCreate']['id']
        )
        PlacementMutationsAPI(
            authorization_in_user_office_with_token).add_placement_metrics_budget_bounces_vimpr_cr_conversions(
            placement_data['data']['placementCreate']['id'],
            metrics_and_conv_data['data']['mplans'][0]['conversions'][0]['id']
        )
        PlacementMutationsAPI(authorization_in_user_office_with_token).setup_placement_completed_status(
            placement_data['data']['placementCreate']['id']
        )
        PlacementMutationsAPI(authorization_in_user_office_with_token).approve_placement(
            mplan_data['data']['mplanPlanningCreate']['id'], placement_data['data']['placementCreate']['id']
        )
        ConnectionSettingsMutationsAPI(
            authorization_in_user_office_with_token).base_setup_placement_connection_settings(
            placement_data['data']['placementCreate']['id']
        )
        PlacementMutationsAPI(authorization_in_user_office_with_token).setup_placement_published_status(
            placement_data['data']['placementCreate']['id']
        )
        time.sleep(10)
        #TODO Поискать замену time.sleep в API методах https://jira.mts.ru/browse/MDP-5983
        reporting_data_api = ReportingQueriesAPI(authorization_in_user_office_with_token).get_reporting_by_campaign_id(
            campaign_id, get_default_campaign_begin_date_for_api(), get_default_campaign_end_date_for_api()
        )
        reporting_data_db = get_digital_report_by_campaign_id(
            campaign_id
        )
        formatted_data_api = reporting_data_handler_api(reporting_data_api)
        formatted_data_db = reporting_data_handler_db(reporting_data_db)
        start_date = datetime.strptime(get_default_campaign_begin_date_for_ui(), "%d.%m.%Y")
        end_date = datetime.strptime(get_default_campaign_end_date_for_ui(), "%d.%m.%Y")
        # Проверка корректности дат и отсутствия лишних:
        assert len(formatted_data_db) == 60
        while start_date <= end_date:
            formatted_date = datetime.strftime(start_date, "%d.%m.%Y")
            assert formatted_date in formatted_data_db
            start_date += timedelta(days=1)
        # Проверка значений метрик за весь период, имеется только в ответе API
        metric_values_all_period = reporting_data_api['data']['digitalReport']['report']['data'][0]['metrics']
        # Проверка значения метрики Бюджет за весь период
        assert round(float(metric_values_all_period[0]), 2) == 999999999.99
        assert int(metric_values_all_period[1]) == 0
        assert int(metric_values_all_period[2]) == 0
        assert int(metric_values_all_period[3]) == 0
        assert round(float(metric_values_all_period[4]), 2) == -999999999.99
        # Проверка значения метрики Отказы за весь период
        assert round(float(metric_values_all_period[5]), 0) == 999
        assert int(metric_values_all_period[6]) == 0
        assert int(metric_values_all_period[7]) == 0
        assert int(metric_values_all_period[8]) == 0
        assert round(float(metric_values_all_period[9]), 0) == -999
        # Проверка значения метрики Показы(видимые) за весь период
        assert round(float(metric_values_all_period[10]), 0) == 999999
        assert int(metric_values_all_period[11]) == 0
        assert int(metric_values_all_period[12]) == 0
        assert int(metric_values_all_period[13]) == 0
        assert round(float(metric_values_all_period[14]), 0) == -999999
        # Проверка значения метрики Конверсии за весь период
        assert round(float(metric_values_all_period[15]), 0) == 9999
        assert int(metric_values_all_period[16]) == 0
        assert int(metric_values_all_period[17]) == 0
        assert round(float(metric_values_all_period[18]), 0) == -9999
        # Проверка значения метрики CR за весь период
        assert round(float(metric_values_all_period[19]), 2) == 99.99
        assert int(metric_values_all_period[20]) == 0
        assert int(metric_values_all_period[21]) == 0
        assert round(float(metric_values_all_period[22]), 2) == -99.99
        # Проверка расчета значений метрик в БД за каждую дату
        for date, metrics in formatted_data_db.items():
            # Проверка значения метрики Бюджет за каждую дату
            assert metrics['BUDGET'][0] == 999999999.99 / len(formatted_data_db)
            assert metrics['BUDGET'][1] == 0
            assert metrics['BUDGET'][2] == 0
            assert metrics['BUDGET'][3] == 0
            assert metrics['BUDGET'][4] == -metrics['BUDGET'][0]
            # Проверка значения метрики Отказы за каждую дату
            assert metrics['BOUNCES'][0] == 999 / len(formatted_data_db)
            assert metrics['BOUNCES'][1] == 0
            assert metrics['BOUNCES'][2] == 0
            assert metrics['BOUNCES'][3] == 0
            assert metrics['BOUNCES'][4] == -metrics['BOUNCES'][0]
            # Проверка значения метрики Показы(видимые) за каждую дату
            assert metrics['VIMPR'][0] == 999999 / len(formatted_data_db)
            assert metrics['VIMPR'][1] == 0
            assert metrics['VIMPR'][2] == 0
            assert metrics['VIMPR'][3] == 0
            assert metrics['VIMPR'][4] == -metrics['VIMPR'][0]
            # Проверка значения метрики CR за каждую дату
            assert metrics['CR'][0] == 99.99
            assert metrics['CR'][1] == 0
            assert metrics['CR'][2] == 0
            assert metrics['CR'][3] == -metrics['CR'][0]
            # Проверка значения метрики конверсии за каждую дату
            assert metrics['CONV'][0] == 9999 / len(formatted_data_db)
            assert metrics['CONV'][1] == 0
            assert metrics['CONV'][2] == 0
            assert metrics['CONV'][3] == -metrics['CONV'][0]
        # Проверка соответствия данных отчета в БД и API
        assert (
                formatted_data_db == formatted_data_api
        )
