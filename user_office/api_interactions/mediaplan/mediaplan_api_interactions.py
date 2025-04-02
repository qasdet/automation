import logging
from random import randint

import allure

from helper.subfield_selections import mplan_subfields
from http_methods.post import post_request
from pathlib import Path
import textwrap

this_dir = Path(__file__).resolve().parent

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filename=f'{this_dir}/api.log',
    filemode='w',
)


class MplanQueriesAPI:
    def __init__(self, token):
        self.token = token

    def get_mplan_id_query(self, campaign_id: str) -> str:
        """ Отправка запроса на сервер для получения идентификатора медиаплана
        Args:
            campaign_id: уникальный идентификатор рекламной кампании
        Returns:
            Возвращает уникальный идентификатор медиаплана в рекламной кампании
        """
        query = {
            'operation_name': 'Mplans',
            'variables': {'filter': {'campaignID': f'{campaign_id}'}},
            'query': 'query Mplans($filter: MplanFilter) {mplans(filter: $filter)'
                     ' {id campaign {id} }}',
        }
        result = post_request(query, token=self.token)
        return result["data"]["mplans"][0]["id"]

    def get_all_mplans_in_campaign(self, campaign_id: str) -> str:
        """ Отправка запроса на сервер для получения идентификаторов медиапланов
                Args:
                    campaign_id: уникальный идентификатор рекламной кампании
                Returns:
                    Возвращает уникальные идентификаторы медиапланов в рекламной кампании
                """
        query = {
            'operation_name': 'Mplans',
            'variables': {
                "slice": {
                    "limit": 6,
                    "offset": 0
                },
                "filter": {
                    "campaignID": [
                        campaign_id
                    ]
                }
            },
            'query': """query Mplans($id: ID, $filter: MplanFilter, $slice: ListSlice) {
                          mplans(id: $id, filter: $filter, slice: $slice) {
                            id
                          }
                        }""",
        }
        ids = post_request(query, token=self.token)
        return ids

    def get_mplan_by_id(self, mplan_id: str) -> dict:
        """Получить данные медиаплана по id
            Args:
                mplan_id: id медиаплана
            Returns:
                Массив данных медиаплана
        """
        query = {
            'variables': {
                'id': mplan_id,
            },
            'query': """query Mplans($id: ID, $filter: MplanFilter, $slice: UserOfficeSlice) {
                        mplans(id: $id, filter: $filter, slice: $slice) """ + mplan_subfields,
        }
        response = post_request(query=query, token=self.token)
        logging.info(f"API RESPONSE mplan_id {response['data']['mplans'][0]['id']}")
        return response

    def get_data_from_mplan(self, campaign_id: str) -> dict:
        """Отправка запроса на сервер для получения некоторых данных по медиаплану
        Args:
            campaign_id: уникальный идентификатор рекламной кампании
        Returns:
            Возвращает часть данных о медиаплане
        """
        query = {
            'operation_name': 'Mplans',
            'variables': {'filter': {'campaignID': f'{campaign_id}'}},
            'query': 'query Mplans($filter: MplanFilter) {mplans(filter: $filter) {id goal {name}}}',
        }
        result = post_request(query, self.token)
        return result['data']

    def get_mplan_status(self, mplan_id: str) -> dict:
        """Получить статус медиаплана по id
            Args:
                mplan_id: id медиаплана
            Returns:
                Статус медиаплана
        """
        query = {
            'variables': {'id': f'{mplan_id}'},
            'query': 'query MplansForView($id: ID!) {mplans(id: $id) { status { code name __typename } __typename } }',
        }
        response = post_request(query=query, token=self.token)
        with allure.step(
                title=f'Checking that {textwrap.shorten(str(response), width=80, placeholder="...")} is get_mplan_by_id'
        ):
            logging.info(f'API RESPONSE {textwrap.shorten(str(response), width=80, placeholder="...")}')
        return response


class MplansMutationsAPI:
    def __init__(self, token):
        self.token = token

    def create_conversion_in_mplan(self, mplan_id, conversion_name):
        """Создание одной конверсии в медиаплане
                    Args:
                        mplan_id: id медиаплана
                        conversion_name: имя создаваемой конверсии
                """
        query = {
            'variables': {
                "data": {
                    "mplanID": mplan_id,
                    "name": conversion_name,
                }
            },
            'query': """mutation MplanConversionCreate($data: MplanConversionData!) {
                          mplanConversionCreate(data: $data) {
                            id
                            name
                            __typename
                          }
                        }"""
        }
        response = post_request(query=query, token=self.token)
        with allure.step(
                title=f'Checking that {textwrap.shorten(str(response), width=80, placeholder="...")} '
                      f'is create_conversion_in_mplan'
        ):
            logging.info(f"API RESPONSE create_conversion_in_mplan {response}")
        return response

    def create_draft_mplan_part(self, campaign_id: str) -> dict:
        """Создание черновика медиаплана. Без заполнения полей
            Args:
                campaign_id: id кампании
            Returns:
                Массив данных созданного черновика медиаплана
        """
        query = {
            'variables': {
                "campaignID": campaign_id
            },
            'query': """mutation MplanDraftCreate($campaignID: ID!, $landings: [String!], $constraints: 
                                [MplanConstraintData!]) { mplanDraftCreate( data: {campaignID: $campaignID, 
                                landings: $landings, constraints: $constraints}) """ + mplan_subfields,
        }
        response = post_request(query=query, token=self.token)
        with allure.step(
                title=f'Checking that {textwrap.shorten(str(response), width=80, placeholder="...")} '
                      f'is create_draft_mplan_part'
        ):
            logging.info(f"API RESPONSE CREATE draft mplan part {response['data']['mplanDraftCreate']['id']}")
        return response

    def create_draft_mplan_full(self, campaign_id: str, digital_test_data: dict) -> dict:
        """Создание черновика медиаплана. Все поля заполнены
            Args:
                campaign_id: id кампании
                digital_test_data: массив тестовых данных для добавления целевой метрики
            Returns:
                Массив данных созданного черновика медиаплана
        """
        query = {
            'variables': {
                "campaignID": campaign_id,
                "constraints": [
                    {
                        "metricCode": digital_test_data['budget_metric_code'],
                        "operation": "gt",
                        "value": str(randint(0, 99999))
                    }
                ],
                "landings": [
                    "https://yandex.ru"
                ]
            },
            'query': """mutation MplanDraftCreate($campaignID: ID!, $landings: [String!], $constraints: 
                                [MplanConstraintData!]) { mplanDraftCreate( data: {campaignID: $campaignID, 
                                landings: $landings, constraints: $constraints}) """ + mplan_subfields,
        }
        response = post_request(query=query, token=self.token)
        with allure.step(
                title=f'Checking that {textwrap.shorten(str(response), width=80, placeholder="...")} is '
                      f'create_draft_mplan_full'
        ):
            logging.info(f"API RESPONSE CREATE: draft mplan full {response['data']['mplanDraftCreate']['id']}")
        return response

    def create_mplan_part(self, campaign_id: str) -> dict:
        """Создание медиаплана. Без заполнения полей
            Args:
                campaign_id: id кампании
            Returns:
                Массив данных созданного медиаплана
        """
        query = {
            'variables': {
                "campaignID": campaign_id
            },
            'query': """mutation MplanPlanningCreate($campaignID: ID!, $landings: [String!], $constraints: 
                                [MplanConstraintData!]) { mplanPlanningCreate( data: {campaignID: $campaignID, 
                                landings: $landings, constraints: $constraints}) """ + mplan_subfields,
        }
        response = post_request(query=query, token=self.token)
        with allure.step(
                title=f'Checking that {textwrap.shorten(str(response), width=80, placeholder="...")} is '
                      f'create_mplan_part'
        ):
            logging.info(f"API RESPONSE: create mplan part {response['data']['mplanPlanningCreate']['id']}")
        return response

    def create_mplan_full(self, campaign_id: str, digital_test_data: dict) -> dict:
        """Создание медиаплана. Все поля заполнены
            Args:
                campaign_id: id кампании
                digital_test_data: массив тестовых данных для добавления целевой метрики
            Returns:
                Массив данных созданного медиаплана
        """
        query = {
            'variables': {
                "campaignID": campaign_id,
                "constraints": [
                    {
                        "metricCode": digital_test_data['metric_code_imps'],
                        "operation": "gt",
                        "value": str(randint(0, 99999))
                    }
                ],
                "landings": [
                    "https://yandex.ru"
                ]
            },
            'query': """mutation MplanPlanningCreate($campaignID: ID!, $landings: [String!], $constraints: 
                                [MplanConstraintData!]) { mplanPlanningCreate( data: {campaignID: $campaignID, 
                                landings: $landings, constraints: $constraints}) """ + mplan_subfields,
        }
        response = post_request(query=query, token=self.token)
        with allure.step(
                title=f'Checking that {textwrap.shorten(str(response), width=80, placeholder="...")} is '
                      f'create_mplan_full'
        ):
            logging.info(
                f'API RESPONSE: create mplan full {textwrap.shorten(str(response), width=80, placeholder="...")}')
        return response

    def update_draft_mplan(self, campaign_id: str, mplan_id: str, digital_test_data: dict) -> dict:
        """Редактирование черновика медиаплана
            Args:
                campaign_id: id кампании
                mplan_id: id медиаплана
                digital_test_data: массив тестовых данных для изменения целевой метрики
            Returns:
                Массив данных отредактированного медиаплана
        """
        query = {
            'variables': {
                "id": mplan_id,
                "campaignID": campaign_id,
                "constraints": [
                    {
                        "metricCode": digital_test_data['metric_code_clicks'],
                        "operation": "gt",
                        "value": str(randint(0, 99999))
                    }
                ],
                "landings": [
                    "https://google.com"
                ]
            },
            'query': """mutation MplanDraftSave($campaignID: ID!, $landings: [String!], $constraints: 
                                [MplanConstraintData!]) { mplanDraftSave( data: {campaignID: $campaignID, 
                                landings: $landings, constraints: $constraints}) """ + mplan_subfields,
        }
        response = post_request(query=query, token=self.token)
        with allure.step(
                title=f'Checking that {textwrap.shorten(str(response), width=80, placeholder="...")} is '
                      f'update_draft_mplan'
        ):
            logging.info(
                f'API RESPONSE: update draft mplan  {textwrap.shorten(str(response), width=80, placeholder="...")}')
        return response
