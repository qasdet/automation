import logging
import textwrap
import allure

from random import randint
from helper.subfield_selections import campaign_subfields
from http_methods.post import post_request
from helper.default_dates import (
    get_default_campaign_begin_date_for_api,
    get_default_campaign_end_date_for_api,
)
from pathlib import Path

this_dir = Path(__file__).resolve().parent

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filename=f'{this_dir}/api.log',
    filemode='w',
)


class CampaignsQueriesAPI:
    def __init__(self, token):
        self.token = token

    def get_all_list_campaigns(self):
        query = {
            'query': """
          query Campaigns($id: ID, $filter: CampaignFilter, $slice: ListSlice) {
                      campaigns(id: $id, filter: $filter, slice: $slice) """ + campaign_subfields
        }
        response = post_request(query=query, token=self.token)
        campaigns_data = response.get('data', []).get('campaigns', [])
        campaigns = []
        for i in campaigns_data:
            campaigns.append(
                {
                    'id': i.get('id'),
                    'name': i.get('name'),
                    'code': i.get('code'),
                }
            )
        return sorted(campaigns, key=lambda x: x['id'])

    def get_campaign_by_id(self, campaign_id: str):
        query = {
            'variables': {
                'id': campaign_id,
            },
            'query': """query Campaigns($id: ID, $filter: CampaignFilter) {
            campaigns(id: $id, filter: $filter) """ + campaign_subfields,
        }
        response = post_request(query=query, token=self.token)
        with allure.step(
                title=f'Checking that {response} is get uuid campaign'
        ):
            logging.info(f'API RESPONSE: get_campaign_id {response}')
        return response

    def get_data_from_ad_campaign(self, campaign_id: str) -> dict:
        """Отправка запроса на сервер для получения некоторых данных по рекламной кампании
        Args:
            campaign_id: уникальный идентификатор рекламной кампании
        Returns:
            Возвращает часть данных о рекламной кампании
        """
        query = {
            'operation_name': 'Campaigns',
            'variables': {'id': f'{campaign_id}'},
            'query': 'query Campaign($id: ID) {campaigns(id: $id) {id name code client {name} brand {name} '
                     'product {name} startOn finishOn}}',
        }
        result = post_request(query, token=self.token)
        return result['data']


class CampaignsMutationsAPI:
    def __init__(self, token):
        self.token = token

    def create_draft_campaign_part(self, data_for_campaign: dict):
        mutation_query = {
            'variables': {
                'clientID': data_for_campaign['client_id'],
                'code': data_for_campaign['campaign_naming'],
                'name': data_for_campaign['campaign_name'],
                'brandID': data_for_campaign['brand_id'],
                'productID': data_for_campaign['product_id'],
                'startOn': f'{get_default_campaign_begin_date_for_api()}T21:00:00.000Z',
                'finishOn': f'{get_default_campaign_end_date_for_api()}T21:00:00.000Z',
                'action': 'DRAFT'
            },
            'query': """mutation campaignCreate($name: String!, $code: String, $brandID: ID!, 
                                             $productID: ID!, $clientID: ID!, $agencyID: ID, $startOn: Time, 
                                             $finishOn: Time, $targetAudience: String, $conditions: String
                                             $action: CampaignCreateAction!) {
        campaignCreate(
        data: {name: $name, brandID: $brandID, productID: $productID, clientID: $clientID, 
        agencyID: $agencyID, startOn: $startOn, finishOn: $finishOn, targetAudience: $targetAudience, 
        conditions: $conditions, code: $code}
        action: $action
        ) """ + campaign_subfields,
        }
        response = post_request(query=mutation_query, token=self.token)
        draft_campaign_id = response['data']['campaignCreate']['id']
        with allure.step(
                title=f'Checking that {draft_campaign_id} is uuid create draft campaign'
        ):
            logging.info(f'API RESPONSE: create draft campaign id {draft_campaign_id}')
        return draft_campaign_id

    def create_draft_campaign_full(self, data_for_campaign: dict):
        mutation_query = {
            'variables': {
                'clientID': data_for_campaign['client_id'],
                'code': data_for_campaign['campaign_naming'],
                'name': data_for_campaign['campaign_name'],
                'brandID': data_for_campaign['brand_id'],
                'productID': data_for_campaign['product_id'],
                'coBrands': data_for_campaign['co_brand_id'],
                'conditions': 'This is a conditions description',
                'targetGeo': 'This is a geo targeting description',
                'targetAudience': 'This is a target audience description',
                'agencyID': data_for_campaign['agency_id'],
                'departmentID': data_for_campaign['department_id'],
                'budget': str(randint(0, 99999999)),
                'startOn': f'{get_default_campaign_begin_date_for_api()}T21:00:00.000Z',
                'finishOn': f'{get_default_campaign_end_date_for_api()}T21:00:00.000Z',
                'action': 'DRAFT'
            },
            'query': """mutation campaignCreate($name: String!, $code: String, $brandID: ID!, 
                                             $productID: ID!, $clientID: ID!, $agencyID: ID, $startOn: Time, 
                                             $finishOn: Time, $targetAudience: String, $conditions: String
                                             $action: CampaignCreateAction!) {
        campaignCreate(
        data: {name: $name, brandID: $brandID, productID: $productID, clientID: $clientID, 
        agencyID: $agencyID, startOn: $startOn, finishOn: $finishOn, targetAudience: $targetAudience, 
        conditions: $conditions, code: $code}
        action: $action
        ) """ + campaign_subfields,
        }
        response = post_request(query=mutation_query, token=self.token)
        draft_campaign_id = response['data']['campaignCreate']['id']
        with allure.step(
                title=f'Checking that {draft_campaign_id} is uuid create draft campaign full'
        ):
            logging.info(f'API RESPONSE: create draft campaign id {draft_campaign_id}')
        return draft_campaign_id

    def create_campaign_part(self, data_for_campaign: dict):
        mutation_query = {
            'variables': {
                'clientID': data_for_campaign['client_id'],
                'code': data_for_campaign['campaign_naming'],
                'name': data_for_campaign['campaign_name'],
                'brandID': data_for_campaign['brand_id'],
                'productID': data_for_campaign['product_id'],
                'startOn': f'{get_default_campaign_begin_date_for_api()}T21:00:00.000Z',
                'finishOn': f'{get_default_campaign_end_date_for_api()}T21:00:00.000Z',
                'action': 'PLANNING'
            },
            'query': """mutation campaignCreate($name: String!, $code: String!,
                                            $brandID: ID!, 
                                            $productID: ID!, $startOn: Time!, $finishOn: Time!, $clientID: ID!, 
                                            $agencyID: ID, $targetAudience: String, $conditions: String
                                            $action: CampaignCreateAction!) {
                campaignCreate(
                data: {name: $name, brandID: $brandID, productID: $productID, 
                clientID: $clientID, startOn: $startOn, finishOn: $finishOn, agencyID: $agencyID, 
                targetAudience: $targetAudience, 
                conditions: $conditions, code: $code}
                action: $action
                ) """ + campaign_subfields,
        }
        response = post_request(query=mutation_query, token=self.token)
        campaign_id = response['data']['campaignCreate']['id']
        with allure.step(
                title=f'Checking that {campaign_id} is uuid create part campaign'
        ):
            logging.info(f'API RESPONSE: part campaign id {campaign_id}')
        return campaign_id

    def create_campaign_part_with_two_co_brands(self, data_for_campaign: dict) -> dict:
        """Создание кампании с 2 ко брендами
            Args:
                data_for_campaign: массив тестовых данных
            Returns:
                Массив данных созданной кампании с 2 ко брендами"""
        create_campaign_query = {
            'variables': {
                'clientID': data_for_campaign['client_id'],
                'code': data_for_campaign['campaign_naming'],
                'name': data_for_campaign['campaign_name'],
                'brandID': data_for_campaign['brand_id'],
                'coBrands': [
                    data_for_campaign['co_brand_id'],
                    data_for_campaign['second_co_brand_id']
                ],
                'productID': data_for_campaign['product_id'],
                'startOn': f'{get_default_campaign_begin_date_for_api()}T21:00:00.000Z',
                'finishOn': f'{get_default_campaign_end_date_for_api()}T21:00:00.000Z',
                'action': 'PLANNING'
            },
            'query': """mutation campaignCreate($name: String!, $code: String!,
                                            $brandID: ID!, $coBrands: [ID!],
                                            $productID: ID!, $startOn: Time!, $finishOn: Time!, $clientID: ID!, 
                                            $agencyID: ID, $targetAudience: String, $conditions: String
                                            $action: CampaignCreateAction!) {
                campaignCreate(
                data: {name: $name, brandID: $brandID, productID: $productID, coBrands: $coBrands,
                clientID: $clientID, startOn: $startOn, finishOn: $finishOn, agencyID: $agencyID, 
                targetAudience: $targetAudience, 
                conditions: $conditions, code: $code}
                action: $action
                ) """ + campaign_subfields,
        }
        response = post_request(query=create_campaign_query, token=self.token)
        with allure.step(
                title=f'Checking that {response} is uuid create part campaign with two co brands'
        ):
            logging.info(f'API RESPONSE: campaign data with two co brands {response}')
        return response

    def create_campaign_part_with_budget(self, data_for_campaign: dict):
        mutation_query = {
            'variables': {
                'clientID': data_for_campaign['client_id'],
                'code': data_for_campaign['campaign_naming'],
                'name': data_for_campaign['campaign_name'],
                'brandID': data_for_campaign['brand_id'],
                'productID': data_for_campaign['product_id'],
                'budget': str(randint(1000000, 9999999)),
                'startOn': f'{get_default_campaign_begin_date_for_api()}T21:00:00.000Z',
                'finishOn': f'{get_default_campaign_end_date_for_api()}T21:00:00.000Z',
                'action': 'PLANNING'
            },
            'query': """mutation campaignCreate($name: String!, $code: String!,
                                            $brandID: ID!, $productID: ID!, $budget: Decimal, $startOn: Time!, 
                                            $finishOn: Time!, $clientID: ID!, $agencyID: ID, $targetAudience: String, 
                                            $conditions: String, $action: CampaignCreateAction!) {
                campaignCreate(
                data: {name: $name, brandID: $brandID, productID: $productID, 
                clientID: $clientID, budget: $budget, startOn: $startOn, finishOn: $finishOn, agencyID: $agencyID, 
                targetAudience: $targetAudience, 
                conditions: $conditions, code: $code}
                action: $action
                ) """ + campaign_subfields,
        }
        response = post_request(query=mutation_query, token=self.token)
        with allure.step(
                title=f'Checking that {response} is create_campaign_part_with_budget'
        ):
            logging.info(f'API RESPONSE: create part campaign with budget {response}')
        return response

    def create_campaign_full(self, data_for_campaign: dict):
        mutation_query = {
            'variables': {
                'clientID': data_for_campaign['client_id'],
                'code': data_for_campaign['campaign_naming'],
                'name': data_for_campaign['campaign_name'],
                'brandID': data_for_campaign['brand_id'],
                'productID': data_for_campaign['product_id'],
                'coBrands': data_for_campaign['co_brand_id'],
                'conditions': 'This is a conditions description',
                'targetGeo': 'This is a geo targeting description',
                'targetAudience': 'This is a target audience description',
                'agencyID': data_for_campaign['agency_id'],
                'departmentID': data_for_campaign['department_id'],
                'budget': str(randint(0, 99999999)),
                'startOn': f'{get_default_campaign_begin_date_for_api()}T21:00:00.000Z',
                'finishOn': f'{get_default_campaign_end_date_for_api()}T21:00:00.000Z',
                'action': 'PLANNING'
            },
            'query': """mutation campaignCreate($name: String!, $code: String!,  $brandID: ID!, 
                                                $coBrands: [ID!], $departmentID: ID, $budget: Decimal, $productID: ID!,
                                                $startOn: Time!, $finishOn: Time!, $clientID: ID!, $agencyID: ID, 
                                                $targetAudience: String, $conditions: String, 
                                                $action: CampaignCreateAction!) {
            campaignCreate(
            data: {name: $name,  brandID: $brandID, productID: $productID, 
                   clientID: $clientID, 
                   startOn: $startOn, finishOn: $finishOn, agencyID: $agencyID, targetAudience: $targetAudience, 
                   conditions: $conditions, code: $code, coBrands: $coBrands, departmentID: $departmentID, 
                   budget: $budget} action: $action
                ) """ + campaign_subfields,
        }
        response = post_request(query=mutation_query, token=self.token)
        campaign_id = response['data']['campaignCreate']['id']
        with allure.step(
                title=f'Checking that {campaign_id} is uuid create full campaign'
        ):
            logging.info(f'API RESPONSE: campaign id {campaign_id}')
        return campaign_id

    def update_campaign_part(self, campaign_id: str, data_for_campaign: dict):
        mutation_query = {
            'variables': {"name": data_for_campaign["new_campaign_name"],
                          "id": campaign_id,
                          "code": data_for_campaign["new_campaign_naming"],
                          "clientID": data_for_campaign["client_id"],
                          "brandID": data_for_campaign["brand_id"],
                          "productID": data_for_campaign["product_id"],
                          'startOn': f'{get_default_campaign_begin_date_for_api()}T21:00:00.000Z',
                          'finishOn': f'{get_default_campaign_end_date_for_api()}T21:00:00.000Z',
                          },
            'query': """mutation campaignUpdate($name: String!, $code: String!, $id: ID!, $startOn: Time, 
                                $finishOn: Time, $clientID: ID!, $brandID: ID!, $productID: ID!) {campaignUpdate(
                                data: {name: $name, code: $code, startOn: $startOn, finishOn: $finishOn, 
                                clientID: $clientID, brandID: $brandID, productID: $productID} id: $id) """
                     + campaign_subfields,
        }
        response = post_request(query=mutation_query, token=self.token)
        with allure.step(
                title=f'Checking that {textwrap.shorten(str(response), width=80, placeholder="...")} is update campaign part'
        ):
            logging.info(
                f'API RESPONSE: update campaign part: {textwrap.shorten(str(response), width=80, placeholder="...")}')
        return response

    def update_campaign_full(self, campaign_id: str, data_for_campaign: dict):
        mutation_query = {
            'variables': {"name": data_for_campaign["new_campaign_name"],
                          "id": campaign_id,
                          "code": data_for_campaign["new_campaign_naming"],
                          "clientID": data_for_campaign["new_client_id"],
                          "brandID": data_for_campaign["new_brand_id"],
                          "coBrands": data_for_campaign["new_co_brand_id"],
                          "productID": data_for_campaign["new_product_id"],
                          'agencyID': data_for_campaign["new_agency_id"],
                          'budget': str(randint(0, 99999999)),
                          "startOn": f'{get_default_campaign_begin_date_for_api()}T21:00:00.000Z',
                          "finishOn": f'{get_default_campaign_end_date_for_api()}T21:00:00.000Z'
                          },
            'query': """mutation campaignUpdate($name: String!, $code: String!, $id: ID!, $startOn: Time, $finishOn: Time, 
                                          $clientID: ID!, $brandID: ID!, $productID: ID!, $coBrands: [ID!], 
                                          $agencyID: ID, $budget: Decimal) {campaignUpdate(data: {name: $name, 
                                          code: $code, startOn: $startOn, finishOn: $finishOn, clientID: $clientID, 
                                          brandID: $brandID, productID: $productID, coBrands: $coBrands, 
                                          budget: $budget, agencyID: $agencyID} id: $id) """ + campaign_subfields,
        }
        response = post_request(query=mutation_query, token=self.token)
        with allure.step(
                title=f'Checking that {textwrap.shorten(str(response), width=80, placeholder="...")} is uuid update full campaign'
        ):
            logging.info(
                f'API RESPONSE: update campaign full: {textwrap.shorten(str(response), width=80, placeholder="...")}')
        return response
