import allure
import pytest
import random

from helper.linkshort import AllureLink as case
from helper.linkshort import JiraLink as jira
from helper.url_constructor import DigitalUrl
from helper.value_handler import value_handler
from user_office.components.pages.dictionaries.dictionaries_page import (
    DictionariesPage
)


@pytest.mark.usefixtures('authorization_in_user_office_with_token')
class TestPlacementTemplates:
    @staticmethod
    @allure.title(test_title='Тест создания шаблона размещения в разделе Справочники')
    @allure.severity(severity_level=allure.severity_level.NORMAL)
    @allure.issue(jira.JIRA_LINK + 'MDP-6337')
    @allure.testcase(case.ALLURE_LINK + '351977?treeId=288')
    @pytest.mark.smoke
    def test_create_placement_template(
            digital_test_data,
            dictionaries: DictionariesPage,
            office_base_url: str,
            delete_placement_template_by_id_in_organization
    ) -> None:
        url = DigitalUrl.get_url_dictionaries_page(
            office_base_url,
            naming='/naming/'
        )
        metric_value = str(value_handler(random.randint(10000, 100000)))
        dictionaries.visit(url)
        dictionaries.dictionaries_page.open_placement_templates_list()
        dictionaries.dictionaries_page.open_create_placement_template_page()
        dictionaries.digital_placement_template.fill_placement_template(digital_test_data, metric_value)
        dictionaries.digital_placement_template.get_back_from_placement_template_page()
        dictionaries.dictionaries_page.check_not_saved_placement_template_in_placement_templates_list(digital_test_data)
        dictionaries.dictionaries_page.open_create_placement_template_page()
        dictionaries.digital_placement_template.fill_placement_template(digital_test_data, metric_value)
        dictionaries.digital_placement_template.save_placement_template()
        dictionaries.dictionaries_page.check_saved_placement_template_in_placement_templates_list(digital_test_data)
        dictionaries.dictionaries_page.open_placement_template_through_context_menu()
        dictionaries.digital_placement_template.check_saved_placement_template(metric_value, digital_test_data)

    @staticmethod
    @allure.title(test_title='Тест редактирования шаблона размещения в разделе Справочники')
    @allure.severity(severity_level=allure.severity_level.NORMAL)
    @allure.issue(jira.JIRA_LINK + 'MDP-6340')
    @allure.testcase(case.ALLURE_LINK + '351974?treeId=288')
    @pytest.mark.regress
    def test_update_placement_template(
            digital_test_data,
            dictionaries: DictionariesPage,
            office_base_url: str,
            delete_placement_template_by_id_in_organization
    ) -> None:
        url = DigitalUrl.get_url_dictionaries_page(
            office_base_url,
            naming='/naming/'
        )
        metric_value = str(value_handler(random.randint(10000, 100000)))
        dictionaries.visit(url)
        dictionaries.dictionaries_page.open_placement_templates_list()
        dictionaries.dictionaries_page.open_create_placement_template_page()
        dictionaries.digital_placement_template.fill_placement_template_base_fields(digital_test_data)
        dictionaries.digital_placement_template.save_placement_template()
        dictionaries.dictionaries_page.check_saved_placement_template_in_placement_templates_list_base_fields(
            digital_test_data
        )
        dictionaries.dictionaries_page.open_placement_template_through_context_menu()
        dictionaries.digital_placement_template.check_saved_placement_template_base_fields(digital_test_data)
        dictionaries.digital_placement_template.fill_placement_template_additional_fields(
            digital_test_data, metric_value
        )
        dictionaries.digital_placement_template.save_placement_template()
        dictionaries.dictionaries_page.check_saved_placement_template_in_placement_templates_list(digital_test_data)
        dictionaries.dictionaries_page.open_placement_template_through_context_menu()

        dictionaries.digital_placement_template.update_placement_template_fields(digital_test_data)
        dictionaries.digital_placement_template.save_placement_template()
        dictionaries.dictionaries_page.check_saved_placement_template_in_placement_templates_list_after_update(
            digital_test_data
        )
        dictionaries.dictionaries_page.open_placement_template_through_context_menu()
        dictionaries.digital_placement_template.check_saved_placement_template_all_fields_after_update(
            digital_test_data, metric_value
        )
