import allure
import logging
import textwrap

from http_methods.post import post_request


class PlacementTemplatesQueriesAPI:
    def __init__(self, token):
        self.token = token

    def get_all_placement_templates(self):
        """Получение всего списка шаблонов размещений"""
        query = {
            'query': """query PlacementTemplates($id: ID) {
                          placementTemplates(id: $id) 
                            {
                              id
                            }
                          }"""
        }
        response = post_request(query=query, token=self.token)
        with allure.step(
                title=f'Checking that '
                      f'{textwrap.shorten(str(response), width=180, placeholder="...")} is get_all_placement_templates'
        ):
            logging.info(
                f'API RESPONSE get placement templates: '
                f'{textwrap.shorten(str(response), width=180, placeholder="...")}'
            )
        return response


class PlacementTemplatesMutationsAPI:
    def __init__(self, token):
        self.token = token

    def delete_placement_template(self, placement_template_id):
        """Удаление шаблона размещения
            Args:
                placement_template_id: id шаблона размещения
            Returns:
                id удаленного шаблона размещения"""
        query = {
            'variables': {
                'templateID': placement_template_id,
            },
            'query': """mutation placementTemplateDelete($templateID: ID!) {
                  placementTemplateDelete(templateID: $templateID)
                }"""
        }
        response = post_request(query=query, token=self.token)
        with allure.step(
                title=f'Checking that '
                      f'{textwrap.shorten(str(response), width=180, placeholder="...")} is delete_placement_templates'
        ):
            logging.info(
                f'API RESPONSE delete placement templates: '
                f'{textwrap.shorten(str(response), width=180, placeholder="...")}'
            )
        return response
