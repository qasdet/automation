import allure
import textwrap
import logging

from http_methods.post import post_request
from helper.subfield_selections import organization_links_subfields


class OrganizationLinksMutationsAPI:
    def __init__(self, token):
        self.token = token

    def create_organization_link(self, organization_link_data: dict):
        """Создание размещения. Заполнены основные поля
        Args:
        mplan_id: id медиаплана
        digital_test_data: словарь тестовых данных
        """
        create_organization_link_query = {
            "variables": {
                "data": {
                    "clientID": organization_link_data["client_id"],
                    "brandID": organization_link_data["brand_id"],
                    "productID": organization_link_data["product_id"]
                }
            },
            "query": """mutation OrganizationLinkCreate($data: OrganizationLinkData!) {
                        organizationLinkCreate(data: $data) """ + organization_links_subfields,
        }
        response = post_request(query=create_organization_link_query, token=self.token)
        with allure.step(
                title=f'Checking that '
                      f'{textwrap.shorten(str(response), width=80, placeholder="...")} is create_organization_link'
        ):
            logging.info(
                f'API RESPONSE CREATE create organization link: '
                f'{textwrap.shorten(str(response), width=80, placeholder="...")}'
            )
        return response
