import logging
import textwrap

import allure

from http_methods.post import post_request
from helper.subfield_selections import reporting_subfields


class ReportingQueriesAPI:
    def __init__(self, token):
        self.token = token

    def get_reporting_by_campaign_id(self, campaign_id: str, start_on: str, finish_on: str):
        """Получить данные отчета план-факт
            Args:
                campaign_id: id кампании
                start_on: дата начала отчета
                finish_on: дата завершения отчета
            Returns:
                Данные отчета план-факт"""
        query = {
            'variables': {
                'id': campaign_id,
                "filter": {
                  "startOn": start_on,
                  "finishOn": finish_on,
                }
            },
            'query': """query DigitalReport($id: ID!, $filter: DigitalReportFilter!) {
                            digitalReport(id: $id, filter: $filter) """ + reporting_subfields,
        }
        response = post_request(query=query, token=self.token)
        with allure.step(
                title=f'Checking that {textwrap.shorten(str(response), width=80, placeholder="...")} is get_reporting_by_campaign_id'
        ):
            logging.info(f'API RESPONSE: get reporting by campaign_id: {textwrap.shorten(str(response), width=80, placeholder="...")}')
        return response
